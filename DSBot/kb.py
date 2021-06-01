import pandas as pd
import json

class KnowledgeBase:
    def __init__(self):
        self.kb = pd.read_excel('kb.xlsx', sheet_name='Foglio2', header=None)
        print(self.kb)
        with open('kb.json') as json_file:
            self.voc = json.load(json_file)