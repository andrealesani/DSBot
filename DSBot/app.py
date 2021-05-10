from flask import Flask, jsonify, request
from flask_restful import reqparse

app = Flask(__name__)

session_id = 1


@app.route('/receiveds', methods=['POST'])
def receive_ds():
    has_index = request.form['has_index']
    has_columns_name = request.form['has_columns_name']

    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        uploaded_file.save(uploaded_file.filename)
        # TODO: apri il file e salvalo

    return {"session_id": session_id}


@app.route('/utterance', methods=['POST'])
def receive_utterance():
    parser = reqparse.RequestParser()
    parser.add_argument('session_id', required=True, type=int, help='No session provided')
    parser.add_argument('message', required=True)
    args = parser.parse_args()

    if (args['session_id'] == session_id):
        pass
        # TODO chhiama nlp su args['message']

        return jsonify({"session_id": session_id,
                        "parsed_requests": [
                            {"operation_id": 1,
                             "request": "Clusterami stocazzo"},
                            {"operation_id": 2,
                             "request": "Faccio la regressione lineare su il numero di utenti per a seconda del mese "
                                        "di nascita"}
                        ]})
    return jsonify({"message": "Errore"})


@app.route('/execute', methods=['POST'])
def execute():
    parser = reqparse.RequestParser()
    parser.add_argument('session_id', required=True, type=int, help='No session provided')
    parser.add_argument('operation_id', required=True, type=int)
    args = parser.parse_args()

    # todo: fai cose

    return jsonify({"message": "ok"})


app.run(port=5000)
