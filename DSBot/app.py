import threading
from functools import partial

# conversation


from DSBot.conversation.fsm.pipelineDrivenConv import pipelineDrivenConv
from DSBot.ir.ir_parameters import IRNumPar
from conversation.fsm.conv import Conv
from conversation.fsm.json_helper import Json_helper
from conversation.fsm.rasa import Rasa

import logging

import flask
from flask import Flask, jsonify, request, send_file, session, send_from_directory
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

#manages first part of conversation: select the type of algorithm (clustering, linear regression, association, ...)
conv = Conv()
#manages second part of conversation: set parameters for each pipeline block
conv2 = pipelineDrivenConv()
#interface to json files where conversations' state is saved
jh = Json_helper()
#helper to interact with Rasa's server end points
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
    filename = None
    if data[session_id] is not None:
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


@app.route('/send-message', methods=['POST'])
def answer_message():
    # get session-id from HTTP request
    parser = reqparse.RequestParser()
    parser.add_argument('session_id', required=True, help='No session provided')
    args = parser.parse_args()
    session_id = args['session_id']
    fsm_response = {}
    # get user's conversation data. If new user, creates one
    if not jh.userConvExists(session_id):
        jh.createConv(session_id)
    state = jh.getstate(session_id)
    part = jh.getpart(session_id)

    # get user input
    json_data = request.get_json(force=True)
    # get intent and entity
    intent, entity = rasa.parse(json_data['payload'])

    # call fsm (1 or 2) and update conv-state
    if part == "1":
        fsm_response = conv.get_response(intent, session_id, state)  # fsm_response is a dictionary with 1 "response" field that is a list of strings
        # check if fsm 1 ended and in case, introduce the first block and ask the first question
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
            print('MAX', max_key)

            ir_tuning = create_IR(
                ["kmeans", "labelRemove", "oneHotEncode", "outliersRemove", "varianceThreshold", "missingValuesRemove",
                 "pca2", "scatterplot", "normalization"])"""
            #TODO creare dinamicamente/randomicamente(giusto per far vedere che supporta diverse pipeline) diverse pipeline
            ir_tuning = create_IR(["missingValuesRemove", "oneHotEncode", "outliersRemove", "varianceThreshold", "kmeans", "pca2", "scatterplot"])
            """#stampa il tipo di oggetto del primo blocco della pipeline
            print(type(ir_tuning[0]))
            x = ir_tuning[0]
            y = x.parameters['eps']
            y.tune_value(0.4)"""
            conv2.addPipeline(session_id, ir_tuning)
            """conv.setConv2(session_id, ir_tuning)
            conv2 = conv.getConv2()"""
            intro = conv2.maxiManager(session_id)
            for s in intro["response"]:
                fsm_response["response"].append(s)
    elif part == "2":
        fsm_response = conv2.conversationHandler(intent, entity, session_id)
    else:
        fsm_response = {"response": ["Oh no! Unfortunately something went wrong please reload the page 🤦‍♀️"]}
    if fsm_response["response"][0] == "Ok, parameter tuning is completed":
        data[session_id]['ir_tuning'] = conv2.pipelines[session_id]
        threading.Thread(target=execute_algorithm, kwargs={'ir': conv2.pipelines[session_id], 'session_id': session_id}).start()
        fsm_response["wf"] = "clustering"
        fsm_response["session_id"] = session_id

    ## TEST SEND IMAGE ##
    # codifico il file in bytecode
    # with open("./conversation/conv_blocks/conv_blocks.png", "rb") as img_file:
    #    my_string = base64.b64encode(img_file.read())
    #    # trasformo il bytecode in stringa
    #    base64_string = my_string.decode('utf-8')
    #fsm_response["image"] = str(base64_string)

    # Return the Bot response to the client
    return fsm_response

# TODO delete it
@app.route('/get-help', methods=['POST'])
def get_help():
    help_message = {}
    # codifico il file in bytecode
    with open("./conversation/conv_blocks/clusters_transformation.png", "rb") as img_file:
        my_string = base64.b64encode(img_file.read())
        # trasformo il bytecode in stringa
        base64_string = my_string.decode('utf-8')
        help_message["image"] = str(base64_string)
        help_message["response"] = "Gathering similar data in groups is also known as clustering and it let's you see similarities between your population, while finding patterns in their features is also known as association and focuses on the correlations between the characteristics of your population. You can see an image of what clustering does on the right panel."
    return help_message


app.run(host='127.0.0.1', port=5000, debug=True)
