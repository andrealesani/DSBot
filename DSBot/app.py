import threading
from functools import partial

# conversation
from DSBot.conversation.fsm.pipelineDrivenConv import pipelineDrivenConv
from conversation.fsm.conv import Conv
from conversation.fsm.json_helper import Json_helper
from conversation.fsm.rasa import Rasa

import logging

import flask
from flask import Flask, jsonify, request, send_file, session
from flask_cors import CORS
from flask_restful import reqparse

from ir.ir import create_IR, run
from log_helpers import setup_logger
from main import Dataset
# from flask_session import Session
from needleman_wunsch import NW
from kb import KnowledgeBase
import os
import pandas as pd
import numpy as np
import importlib
import base64
from threading import Thread
import matplotlib.pyplot as plt
import seaborn as sns
import copy
from datetime import timedelta
from flask.sessions import SecureCookieSessionInterface

from tuning import get_framework

setup_logger()

app = Flask(__name__)
cors = CORS(app, supports_credentials=True)
app.config['SECRET_KEY'] = 'secret!'
app.config['CORS_HEADERS'] = 'application/json'
app.config['CORS_SUPPORTS_CREDENTIALS'] = True

# app.config['SESSION_TYPE'] = 'filesystem'
# session config
# app.config['SESSION_FILE_DIR'] = 'flask_session'
# DEFAULT 31 days
# app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=31)
# Session(app)
session_serializer = SecureCookieSessionInterface().get_signing_serializer(app)
data = {}

conv = Conv()
jh = Json_helper()
rasa = Rasa()


@app.route('/receiveds', methods=['POST'])
def receive_ds():
    session_id = session_serializer.dumps(dict(session))
    data[session_id] = {}
    has_index = 0 if request.form['has_index'] == 'true' else None
    has_columns_name = 0 if request.form['has_column_names'] == 'true' else None
    sep = request.form['separator']
    label = request.form['label']
    # format = request.form['format']
    # print('sep', sep)
    uploaded_file = request.files['ds']
    if uploaded_file.filename != '':
        # uploaded_file.save(uploaded_file.filename)
        try:
            os.makedirs('./temp/temp_' + str(session_id))
        except:
            pass
        uploaded_file.save('./temp/temp_' + str(session_id) + '/' + uploaded_file.filename)
        dataset = pd.read_csv('./temp/temp_' + str(session_id) + '/' + str(uploaded_file.filename),
                              header=has_columns_name, index_col=has_index, sep=sep, engine='python')
        # print(dataset)
        dataset.to_csv('./temp/temp_' + str(session_id) + '/' + uploaded_file.filename)
        dataset = Dataset(dataset)
        dataset.session = session_id
        print(label)

        if label is not None and label != '':
            dataset.set_label(label)
            # dataset.label = label
            # dataset.hasLabel = True
            print('dslabel', dataset.label, dataset.hasLabel)
        dataset.set_characteristics()
        kb = KnowledgeBase()
        kb.kb = dataset.filter_kb(kb.kb)
        data[session_id]['kb'] = kb
        data[session_id]['dataset'] = dataset

    print(kb.kb)
    print("SESSION ID", session_id)
    # print('label', label, dataset.label, dataset.hasLabel)
    return jsonify({"session_id": session_id})


@app.route('/utterance', methods=['POST'])
def receive_utterance():
    # print(dataset.dataset)

    # ds = copy.deepcopy(dataset)
    parser = reqparse.RequestParser()
    parser.add_argument('session_id', required=True, help='No session provided')
    parser.add_argument('message', required=True)
    args = parser.parse_args()
    session_id = args['session_id']
    if session_id in data:
        with open('./temp/temp_' + str(session_id) + '/message' + str(session_id) + '.txt', 'w') as f:
            f.write(args['message'])

        os.system(
            'onmt_translate -model wf/run/model_step_1000.pt -src temp/temp_' + str(session_id) + '/message' + str(
                session_id) + '.txt -output ./temp/temp_' + str(session_id) + '/pred' + str(
                session_id) + '.txt -gpu -1 -verbose')
        # doppione --> non fa nulla
        # with open('./temp/temp_' + str(session_id) + '/pred' + str(session_id) + '.txt', 'r') as f:
        # wf = f.readlines()[0].strip().split(' ')

        with open('./temp/temp_' + str(session_id) + '/pred' + str(session_id) + '.txt', 'r') as f:
            wf = f.readlines()[0].strip().split(' ')
        scores = {}

        kb = data[session_id]['kb']
        print(kb.kb)
        for i in range(len(kb.kb)):
            sent = [x for x in kb.kb.values[i, 1:] if str(x) != 'nan']
            print(sent)
            scores[i] = NW(wf, sent, kb.voc) / len(sent)
            print(scores[i])

        print(scores)
        max_key = max(scores, key=scores.get)
        max_key = [x for x in kb.kb.values[max_key, 1:] if str(x) != 'nan']
        print('MAX', max_key)

        ir_tuning = create_IR(max_key)
        data[session_id]['ir_tuning'] = ir_tuning
        threading.Thread(target=execute_algorithm, kwargs={'ir': ir_tuning, 'session_id': session_id}).start()
        return jsonify({"session_id": session_id,
                        "request": wf})
    return jsonify({"message": "Errore"})


@app.route('/results/<received_id>')
def get_results(received_id):
    session_id = received_id
    app.logger.info('Polling results for session: %s', session_id)

    # recupero il file
    filename = data[session_id]['dataset'].name_plot
    if filename is None:
        return jsonify({"ready": False, "session_id": session_id, 'img': None, 'tuning': None})

    # codifico il file in bytecode
    with open(filename, "rb") as img_file:
        my_string = base64.b64encode(img_file.read())
        # trasformo il bytecode in stringa
        base64_string = my_string.decode('utf-8')

    framework = get_framework(pipeline=data[session_id]['ir_tuning'],
                              result=base64_string,
                              start_work=partial(re_execute_algorithm, session_id=session_id))

    data[session_id]['framework'] = framework
    details = data[session_id]['dataset'].measures
    tuning_data = framework.handle_data_input({})
    return jsonify({"ready": True,
                    "session_id": session_id,
                    'img': str(base64_string),
                    'details': str(details),
                    'tuning': tuning_data})


@app.route('/tuning', methods=['POST'])
def tuning():
    json_data = request.get_json(force=True)
    session_id = json_data['session_id']
    if json_data['type'] == 'utterance':
        response = data[session_id]['framework'].handle_text_input(json_data['utterance'])
    else:
        response = data[session_id]['framework'].handle_data_input(json_data['payload'])
    return jsonify({'tuning': response})


def execute_algorithm(ir, session_id):
    app.logger.debug('Entering execute_algorithm function')
    app.logger.info('Executing pipeline: %s', [i.to_json() for i in ir])
    dataset = data[session_id]['dataset']
    if hasattr(dataset, 'label'):
        results = {'original_dataset': dataset, 'labels': dataset.label}
    else:
        results = {'original_dataset': dataset}
    result = run(ir, results, session_id)

    app.logger.info('Exiting execute_algorithm function')


def re_execute_algorithm(ir, session_id):
    data[session_id]['dataset'].name_plot = None
    threading.Thread(target=execute_algorithm, kwargs={'ir': ir, 'session_id': session_id}).start()


@app.route('/echo', methods=['POST'])
def echo():
    # get session-id from HTTP request
    parser = reqparse.RequestParser()
    parser.add_argument('session_id', required=True, help='No session provided')
    args = parser.parse_args()
    session_id = args['session_id']

    # get user's conversation data, if new user creates one
    if not jh.userConvExists(session_id):
        jh.createConv(session_id)
    state = jh.getstate(session_id)
    part = jh.getpart(session_id)

    # get the most probable intent
    json_data = request.get_json(force=True)
    intent = rasa.parse(json_data['payload'])

    # call fsm and update conv-state
    if part == "1":
        fsm_response = conv.get_response(intent, session_id, state)
        # fsm 1 ended
        if jh.getstate(session_id) == "start_pipeline":

            jh.updatepart(session_id)

            """scores = {}
            kb = data[session_id]['kb']
            print(kb)
            for i in range(len(kb)):
                sent = [x for x in kb.values[i, 1:] if str(x) != 'nan']
                print(sent)
                scores[i] = NW("clustering", sent, kb.voc) / len(sent)
                print(scores[i])

            print(scores)
            max_key = max(scores, key=scores.get)
            max_key = [x for x in kb.kb.values[max_key, 1:] if str(x) != 'nan']
            print('MAX', max_key)"""

            ir_tuning = create_IR(["dbscan","labelRemove","oneHotEncode","outliersRemove","laplace","missingValuesRemove", "pca2", "scatterplot", "normalization"])
            #stampa il tipo di oggetto del primo blocco della pipeline
            print(type(ir_tuning[0]))
            x = ir_tuning[0]
            y = x.parameters['eps']
            z = y.value(0.4)


            conv2 = pipelineDrivenConv(session_id, ir_tuning)




    elif part == "2":
        pass
        #call mini/maxi manager
        #conv2.convHandler(intent, entities, session_id)

    # Return the Bot response to the client
    return fsm_response["response"]




app.run(host='localhost', port=5000, debug=True)

