import threading

import flask
from flask import Flask, jsonify, request, send_file, session
from flask_cors import CORS
from flask_restful import reqparse

from ir.ir import create_IR, run
from log_helpers import setup_logger
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

setup_logger()
kb = KnowledgeBase()
dataset = Dataset(None)
ir_tuning = None

def receive_ds(ds, has_index, has_col ,sep, label):
    global dataset
    has_index = 0 if has_index else None
    has_columns_name = 0 if has_col else None
    sep = sep
    label = label
    #format = request.form['format']
    #print('sep', sep)
    dataset = pd.read_csv(ds, header=has_columns_name, index_col=has_index,  sep=sep, engine='python')
    dataset = Dataset(dataset)
    print(dataset.ds)
    dataset.label = label
    kb.kb = dataset.filter_kb(kb.kb)


receive_ds('penguins.csv',True, True, ',',None)
#ds = copy.deepcopy(dataset)
message = 'find groups in the data'
with open('./message_try.txt', 'w') as f:
    f.write(message)

os.system('onmt_translate -model wf/run/model_step_1000.pt -src ./message_try.txt -output ./wf_try_pred.txt -gpu -1 -verbose')

with open('./wf_try_pred.txt', 'r') as f:
    wf = f.readlines()[0].strip().split(' ')
    print(wf)

# with open('./temp/temp_' + str(session_id) + '/pred' + str(session_id) + '.txt', 'r') as f:
#     wf = f.readlines()[0].strip().split(' ')
scores = {}
for i in range(len(kb.kb)):
    sent = [x for x in kb.kb.values[i, 1:] if str(x) != 'nan']
    print('sent', sent)
    print('wf', wf)
    scores[i] = NW(wf, sent, kb.voc)
    print('scores', scores[i])
max_key = max(scores, key=scores.get)
max_key = [x for x in kb.kb.values[max_key, 1:] if str(x) != 'nan']
print('MAX', max_key)
#
ir_tuning = create_IR(max_key)
print('IRTUNING', [i for i in ir_tuning])