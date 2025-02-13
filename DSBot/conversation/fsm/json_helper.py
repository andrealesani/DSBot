import json
import os


class Json_helper:

    def userConvExists(self, id: str):
        return os.path.exists('./conversation/temp/conv_' + str(id))

    def createConv(self, id: str):
        conv_dict = {"part": "1", "state": "greeting", "predState": "greeting"}
        with open('./conversation/temp/conv_' + str(id), 'x') as f:
            json.dump(conv_dict, f)

    def updatestate(self, id: str, state: str):
        with open('./conversation/temp/conv_' + str(id), 'r') as f:
            updated = json.load(f)
            updated["state"] = state
        with open('./conversation/temp/conv_' + str(id), 'w') as f:
            f.write(json.dumps(updated))

    def updatePredState(self, id: str, predState: str):
        with open('./conversation/temp/conv_' + str(id), 'r') as f:
            updated = json.load(f)
            updated["predState"] = predState
        with open('./conversation/temp/conv_' + str(id), 'w') as f:
            f.write(json.dumps(updated))

    def updatepart(self, id: str, state="intro"):
        with open('./conversation/temp/conv_' + str(id), 'r') as f:
            updated = json.load(f)
            updated["state"] = state
            updated["part"] = "2"
        with open('./conversation/temp/conv_' + str(id), 'w') as f:
            f.write(json.dumps(updated))
    def resetpart(self, id: str, part: int):
        with open('./conversation/temp/conv_' + str(id), 'r') as f:
            updated = json.load(f)
            updated["part"] = str(part)
        with open('./conversation/temp/conv_' + str(id), 'w') as f:
            f.write(json.dumps(updated))
    def getstate(self, id: str):
        with open('./conversation/temp/conv_' + str(id), 'r') as f:
            conv = json.load(f)
            state = conv["state"]
            return state

    def getPredState(self, id: str):
        with open('./conversation/temp/conv_' + str(id), 'r') as f:
            conv = json.load(f)
            predState = conv["predState"]
            return predState

    def getpart(self, id: str):
        with open('./conversation/temp/conv_' + str(id), 'r') as f:
            conv = json.load(f)
            part = conv["part"]
            return part

    def addPipeline(self,id:str, pipeline):
        pipeline = json.dumps(pipeline)
        with open('./conversation/temp/conv_' + str(id), 'r') as f:
            conv = json.load(f)
            conv["pipeline"] = pipeline
        with open('./conversation/temp/conv_' + str(id), 'w') as f:
            f.write(json.dumps(conv))

    def setParamIndex(self, id:str, param:int):
        with open('./conversation/temp/conv_' + str(id), 'r') as f:
            updated = json.load(f)
            updated["param"] = param
        with open('./conversation/temp/conv_' + str(id), 'w') as f:
            f.write(json.dumps(updated))

    def setBlockIndex(self, id: str, block: int):
        with open('./conversation/temp/conv_' + str(id), 'r') as f:
            updated = json.load(f)
            updated["block"] = block
        with open('./conversation/temp/conv_' + str(id), 'w') as f:
            f.write(json.dumps(updated))

    def getParamIndex(self, id: str):
        with open('./conversation/temp/conv_' + str(id), 'r') as f:
            conv = json.load(f)
            param = int(conv["param"])
            return param

    def getBlockIndex(self, id: str):
        with open('./conversation/temp/conv_' + str(id), 'r') as f:
            conv = json.load(f)
            block = int(conv["block"])
            return block

    def getHelp(self, state: str):
        with open('./conversation/conv_blocks/conv1.json') as f:
            helps = json.load(f)
            help = helps[state]
            del help["question"]
            return help

    def getQuestion(self, state:str):
        with open('./conversation/conv_blocks/conv1.json') as f:
            states = json.load(f)
            return states[state]["question"]

    def getBlockHelp(self, block: str, param: int):
        with open('./conversation/conv_blocks/' + block + '.json') as f:
            helps = json.load(f)
            help = helps["parameters"][param]["help"]
            return help

    def reset(self, id):
        self.setParamIndex(id, 0)
        self.setBlockIndex(id, 0)
        self.updatestate(id, "greeting")
        self.resetpart(id, 1)
