import threading

import flask
from flask import Flask, jsonify, request, send_file, session
from flask_cors import CORS
from flask_restful import reqparse

from ir.ir import create_IR, run
from main import Dataset
#from flask_session import Session
from needleman_wunsch import NW
from kb import KnowledgeBase
import os
import pandas as pd
import importlib
import base64
from threading import Thread

import copy
from datetime import timedelta
from flask.sessions import SecureCookieSessionInterface

from tuning import get_framework

app = Flask(__name__)
cors = CORS(app, supports_credentials=True)
app.config['SECRET_KEY'] = 'secret!'
app.config['CORS_HEADERS'] = 'application/json'
app.config['CORS_SUPPORTS_CREDENTIALS']  = True
session_id = 1

#app.config['SESSION_TYPE'] = 'filesystem'
#session config
#app.config['SESSION_FILE_DIR'] = 'flask_session'
# DEFAULT 31 days
#app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=31)
#Session(app)
session_serializer = SecureCookieSessionInterface().get_signing_serializer(app)
kb = KnowledgeBase()
dataset = Dataset(None)
ir_tuning = None
mmcc_instances = {}


@app.route('/receiveds', methods=['POST'])
def receive_ds():
    global session_id
    session_id = session_serializer.dumps(dict(session))
    has_index = 0 if request.form['has_index']=='true' else None
    has_columns_name = 0 if request.form['has_column_names']=='true' else None
    sep = request.form['separator']
    label = request.form['label']
    #format = request.form['format']
    #print('sep', sep)
    uploaded_file = request.files['ds']
    if uploaded_file.filename != '':
        print("si salva!")
        #uploaded_file.save(uploaded_file.filename)
        try:
            os.makedirs('./temp/temp_'+str(session_id))
        except:
            pass
        uploaded_file.save('./temp/temp_'+str(session_id)+'/' + uploaded_file.filename)
        global dataset
        dataset = pd.read_csv('./temp/temp_'+str(session_id)+'/'+str(uploaded_file.filename), header=has_columns_name, index_col=has_index,  sep=sep, engine='python')
        #print(dataset)
        dataset.to_csv('./temp/temp_'+str(session_id)+'/' + uploaded_file.filename)
        dataset = Dataset(dataset)
        print(dataset.ds)
        dataset.session = session_id
        dataset.label = label
        kb.kb = dataset.filter_kb(kb.kb)

    print(kb.kb)
    print("SESSION ID", session_id)
    return jsonify({"session_id": session_id})


@app.route('/utterance', methods=['POST'])
def receive_utterance():
    #print(dataset.dataset)
    global dataset

    #ds = copy.deepcopy(dataset)
    parser = reqparse.RequestParser()
    parser.add_argument('session_id', required=True, help='No session provided')
    parser.add_argument('message', required=True)
    args = parser.parse_args()
    if (args['session_id'] == session_id):
        with open('./temp/temp_'+str(session_id)+'/message'+str(session_id)+'.txt', 'w') as f:
            f.write(args['message'])

        os.system('onmt_translate -model wf/run/model_step_1000.pt -src temp/temp_'+str(session_id)+'/message'+str(session_id)+'.txt -output ./temp/temp_'+str(session_id)+'/pred'+str(session_id)+'.txt -gpu -1 -verbose')

        with open('./temp/temp_' + str(session_id) + '/pred' + str(session_id) + '.txt', 'r') as f:
            wf = f.readlines()[0].strip().split(' ')
        print(wf)

        print(session_id)
        with open('./temp/temp_' + str(session_id) + '/pred' + str(session_id) + '.txt', 'r') as f:
            wf = f.readlines()[0].strip().split(' ')
        scores = {}
        for i in range(len(kb.kb)):
            sent = [x for x in kb.kb.values[i, 1:] if str(x) != 'nan']
        print(sent)
        print(wf)
        scores[i] = NW(wf, sent, kb.voc)
        print(scores[i])
        max_key = max(scores, key=scores.get)
        max_key = [x for x in kb.kb.values[max_key, 1:] if str(x) != 'nan']
        print('MAX', max_key)

        global ir_tuning
        ir_tuning = create_IR(max_key)
        threading.Thread(target=execute_algorithm, kwargs={'ir': ir_tuning}).start()
        return jsonify({"session_id": session_id,
                        "request": wf
                        })
    return jsonify({"message": "Errore"})


@app.route('/results/<received_id>')
def get_results(received_id):
    # recupero il file
    filename = dataset.name_plot
    print(filename)
    if filename is None:
        return jsonify({"ready": False, "session_id": session_id, 'img': None, 'tuning': None})

    # codifico il file in bytecode
    with open(filename, "rb") as img_file:
        my_string = base64.b64encode(img_file.read())
        # trasformo il bytecode in stringa
        base64_string = my_string.decode('utf-8')

    framework = get_framework(pipeline=ir_tuning,
                              result=base64_string,
                              start_work=re_execute_algorithm)

    mmcc_instances[session_id] = framework
    tuning_data = framework.handle_data_input({})
    return jsonify({"ready": True, "session_id": session_id, 'img': str(base64_string), 'tuning': tuning_data})


@app.route('/tuning', methods=['POST'])
def tuning():
    parser = reqparse.RequestParser()
    parser.add_argument('type', required=True)
    parser.add_argument('utterance')
    parser.add_argument('payload')
    args = parser.parse_args()
    if args['type'] == 'utterance':
        response = mmcc_instances[session_id].handle_text_input(args['utterance'])
    else:
        response = mmcc_instances[session_id].handle_data_input(args['payload'])
    return jsonify({'tuning': response})


def execute_algorithm(ir):
    app.logger.debug('Entering execute_algorithm function')
    global dataset
    results = {'original_dataset': dataset.ds, 'labels':dataset.label}
    run(ir, results)
    app.logger.info('Exiting execute_algorithm function')


def re_execute_algorithm(ir):
    global dataset
    dataset.name_plot = None
    threading.Thread(target=execute_algorithm, kwargs={'ir': ir}).start()


app.run(host='0.0.0.0', port=5000, debug=True)
