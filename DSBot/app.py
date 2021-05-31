import flask
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from flask_restful import reqparse
from main import Dataset
from needleman_wunsch import NW
from kb import KnowledgeBase
import os
import pandas as pd
import importlib
import base64
import copy

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'application/json'

session_id = 1

kb = KnowledgeBase()
dataset = Dataset(None)

@app.route('/receiveds', methods=['POST'])
def receive_ds():
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
        uploaded_file.save('./temp/' + uploaded_file.filename)
        global dataset
        dataset = pd.read_csv('./temp/'+str(uploaded_file.filename), header=has_columns_name, index_col=has_index,  sep=sep, engine='python')
        #print(dataset)
        dataset.to_csv('./temp/' + uploaded_file.filename)
        dataset = Dataset(dataset)
        print(dataset.ds)
        dataset.label = label
        kb.kb = dataset.filter_kb(kb.kb)
    print(kb.kb)
    return jsonify({"session_id": session_id})


@app.route('/utterance', methods=['POST'])
def receive_utterance():
    #print(dataset.dataset)

    global dataset
    ds = copy.deepcopy(dataset)
    parser = reqparse.RequestParser()
    parser.add_argument('session_id', required=True, type=int, help='No session provided')
    parser.add_argument('message', required=True)
    args = parser.parse_args()
    if (args['session_id'] == session_id):
        with open('./temp/message'+str(session_id)+'.txt', 'w') as f:
            f.write(args['message'])

        os.system('onmt_translate -model wf/run/model_step_1000.pt -src temp/message'+str(session_id)+'.txt -output temp/pred'+str(session_id)+'.txt -gpu -1 -verbose')

        with open('temp/pred'+str(session_id)+'.txt', 'r') as f:
            wf = f.readlines()[0].strip().split(' ')
        print(wf)
        scores = {}
        print(len(kb.kb))
        print(kb.kb)
        for i in range(len(kb.kb)):
            sent = [x for x in kb.kb.values[i,1:] if str(x) != 'nan']
            print(sent)
            print(wf)
            scores[i] = NW(wf,sent,kb.voc)
            print(scores[i])
        max_key = max(scores, key=scores.get)
        max_key = [x for x in kb.kb.values[max_key, 1:] if str(x) != 'nan']
        print('MAX', max_key)
        for i in max_key:
            package = importlib.import_module('ds_operations')
            print(i)
            logic= getattr(package, i)
            print(logic)
            dataset = logic(ds)



        return jsonify({"session_id": session_id,
                        "request": wf
                        })
    return jsonify({"message": "Errore"})

# NOT USED
@app.route('/execute', methods=['POST'])
def execute():
    parser = reqparse.RequestParser()
    parser.add_argument('session_id', required=True, type=int, help='No session provided')
    parser.add_argument('operation_id', required=True, type=int)
    args = parser.parse_args()
    return jsonify({"message": "ok"})


@app.route('/results/<int:received_id>')
def get_results(received_id):
    print('HEREEEEE')
    # TODO: if(not ready)
    #   return jsonify({"ready": False, "session_id": session_id})
    # recupero il file
    global dataset
    filename = dataset.name_plot
    print(filename)
    if filename!=None:
    # codifico il file in bytecode
        with open(filename, "rb") as img_file:
            my_string = base64.b64encode(img_file.read())
            # trasformo il bytecode in stringa
            base64_string = my_string.decode('utf-8')
    else:
        filename='assets/pepe.png'
        with open(filename, "rb") as img_file:
            my_string = base64.b64encode(img_file.read())
            # trasformo il bytecode in stringa
            base64_string = my_string.decode('utf-8')
    return jsonify({"ready": True, "session_id": session_id, 'img': str(base64_string)})


app.run(port=5000, debug=True)


