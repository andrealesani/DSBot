import json
import os


class Json_helper:

    def userConvExists(self, id: str):
        return os.path.exists('./conversation/temp/conv_' + str(id))

    def createConv(self, id: str):
        conv_dict = {"part": "1", "state": "greeting"}
        with open('./conversation/temp/conv_' + str(id), 'x') as f:
            json.dump(conv_dict, f)

    def updatestate(self, id: str, state: str):
        with open('./conversation/temp/conv_' + str(id), 'r') as f:
            updated = json.load(f)
            updated["state"] = state
        with open('./conversation/temp/conv_' + str(id), 'w') as f:
            f.write(json.dumps(updated))

    def updatepart(self, id: str, state="intro"):
        with open('./conversation/temp/conv_' + str(id), 'r') as f:
            updated = json.load(f)
            updated["state"] = state
            updated["part"] = "2"
        with open('./conversation/temp/conv_' + str(id), 'w') as f:
            f.write(json.dumps(updated))

    def getstate(self, id: str):
        with open('./conversation/temp/conv_' + str(id), 'r') as f:
            conv = json.load(f)
            state = conv["state"]
            return state

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
