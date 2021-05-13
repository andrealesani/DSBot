import flask
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from flask_restful import reqparse
import os
import pandas as pd

import base64

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'application/json'

session_id = 1


@app.route('/receiveds', methods=['POST'])
def receive_ds():
    has_index = 0 if request.form['has_index']=='true' else None
    has_columns_name = 0 if request.form['has_column_names']=='true' else None
    sep = request.form['separator']
    format = request.form['format']

    uploaded_file = request.files['ds']
    if uploaded_file.filename != '':
        print("si salva!")
        #uploaded_file.save(uploaded_file.filename)
        uploaded_file.save('./temp' + uploaded_file.filename)
        global dataset
        dataset = pd.read_csv(str(uploaded_file.filename), header=has_columns_name, index_col=has_index,  sep=sep)
        dataset.to_csv('./temp' + uploaded_file.filename)

    return jsonify({"session_id": session_id})




@app.route('/utterance', methods=['POST'])
def receive_utterance():
    print('ciaoooooo')
    parser = reqparse.RequestParser()
    parser.add_argument('session_id', required=True, type=int, help='No session provided')
    parser.add_argument('message', required=True)
    args = parser.parse_args()

    if (args['session_id'] == session_id):
        with open('temp/message'+str(session_id)+'.txt', 'w') as f:
            f.write(args['message'])

        os.system('onmt_translate -model DSBot/wf/run/model_step_1000.pt -src temp/message'+str(session_id)+'.txt -output temp/pred'+str(session_id)+'.txt -gpu -1 -verbose')

        with open('temp/pred'+str(session_id)+'.txt', 'r') as f:
            wf = f.readlines()
        print(wf)
        return jsonify({"session_id": session_id,
                        "request": "Faccio la regressione lineare su il numero di utenti per a seconda del mese "
                                    "di nascita"
                        })
    return jsonify({"message": "Errore"})


@app.route('/execute', methods=['POST'])
def execute():
    parser = reqparse.RequestParser()
    parser.add_argument('session_id', required=True, type=int, help='No session provided')
    parser.add_argument('operation_id', required=True, type=int)
    args = parser.parse_args()

    # todo: fai cose

    return jsonify({"message": "ok"})


@app.route('/results/<int:received_id>')
def get_results(received_id):
    # TODO: if(not ready)
    #   return jsonify({"ready": False, "session_id": session_id})

    # recupero il file
    filename = "assets/pepe.png"

    # codifico il file in bytecode
    with open(filename, "rb") as img_file:
        my_string = base64.b64encode(img_file.read())
        # trasformo il bytecode in stringa
        base64_string = my_string.decode('utf-8')
    return jsonify({"ready": True, "session_id": session_id, 'img': str(base64_string)})


app.run(port=5000, debug=True)


