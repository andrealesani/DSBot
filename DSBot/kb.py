import pandas as pd

class KnowledgeBase:
    def __init__(self):
        self.kb = pd.read_excel('kb.xlsx',sheet_name=1, header=None)

