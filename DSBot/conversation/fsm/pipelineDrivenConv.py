import json
import os

from DSBot.conversation.fsm.json_helper import Json_helper


class pipelineDrivenConv:

    def __init__(self):
        self.js = Json_helper()
        self.pipelines = {}

    # blockIndex = 0  # indice lista blocchetti da mettere nel json

    # stati-> (introduction,) parametersSetting, endBlock

    # danno errore, perché la pipeline non è serializzabile
    # self.js.addPipeline(session_id, pipeline)
    # self.js.setCurrentBlock(session_id, 0)
    # self.js.setParamIndex(session_id, 0)

    def addPipeline(self, session_id, pipeline):
        self.js.updatestate(session_id, "parametersSetting")
        self.pipelines[session_id] = pipeline
        # self.pipeline = pipeline  # metti pipeline in dizionario
        self.js.setParamIndex(session_id, 0)
        self.js.setBlockIndex(session_id, 0)
        # self.param = 0  # metti in json indice parametro =0

    def conversationHandler(self, intent, entities, session_id):
        pipeline = self.pipelines[session_id]
        blockIndex = self.js.getBlockIndex(session_id)
        paramIndex = self.js.getParamIndex(session_id)

        """if self.js.getstate(session_id) == "intro":
            if intent == "affirm":
                #TODO add detailed explanation in the json
                pass"""

        if self.js.getstate(session_id) == "parametersSetting":
            # with open('./conversation/conv_blocks/' + self.pipeline[self.blockIndex].name + ".json", 'r') as f:
            with open('./conversation/conv_blocks/' + pipeline[blockIndex].name + ".json", 'r') as f:
                block = json.load(f)
            try:
                pipeline[blockIndex].parameters[block["parameters"][paramIndex]["name"]].tune_value(
                    int(entities[0]["value"]))
            except:
                return {"response": "Sorry, I didn't understand"}

            if paramIndex == len(block["parameters"]) - 1:
                self.js.updatestate(session_id, "endBlock")
            else:
                paramIndex += 1
                self.js.setParamIndex(session_id, paramIndex)

            """if block["name"] == "kmeans":
                if (intent == "clustering" or intent == "kmeans") and entities[0]["entity"] == "n_clusters":
                    self.pipeline[self.blockIndex].parameters['n_clusters'].tune_value(int(entities[0]["value"]))
                    self.js.updatestate(session_id, "endBlock")
                else:
                    return {"response": "Sorry, I didn't understand"}"""

            return self.maxiManager(session_id)

    # check(intent, entities, stato)

    # ----->set_parameter
    # modifica stato

    # if stato == fine
    # maximanager ->check

    # else send_response

    def maxiManager (self, session_id):
        # verifica che il blocchetto sia utile e che lo stato non sia fine blocchetto altrimetni prende  # quello
        # dopo (fa anche il check dei parametri) da aggiungere agglomerative variance treshold e outliers(?)
        pipeline = self.pipelines[session_id]
        blockIndex = self.js.getBlockIndex(session_id)
        paramIndex = self.js.getParamIndex(session_id)

        if self.js.getstate(session_id) == "endBlock" or blockIndex == 0:
            blockIndex += 1
            # self.js.setBlockIndex(session_id, blockIndex)
            # self.js.setParamIndex(session_id, 0)
            self.js.updatestate(session_id, "parametersSetting")
            # find next block with parameters to set
            try:
                while not self.hasParameters(pipeline[blockIndex]):
                    # while(pipeline[blockIndex].name != "dbscan" and pipeline[blockIndex].name != "kmeans" and
                    # pipeline[blockIndex].name != "laplace"):
                    blockIndex += 1
            except IndexError:
                return {"response": "Ok, parameter tuning is completed, in a moment you will see the results"}
            self.js.setBlockIndex(session_id, blockIndex)
            self.js.setParamIndex(session_id, 0)

            # send_introduction
            if (blockIndex < len(pipeline)):
                with open('./conversation/conv_blocks/' + pipeline[blockIndex].name + ".json", 'r') as f:
                    block = json.load(f)
                    toReturn = block["description"] + " " + block["parameters"][paramIndex]["question"]
                return {"response": toReturn}
            else:
                return {"response": "Ok, parameter tuning is completed, in a moment you will see the results"}
        elif self.hasParameters(pipeline[blockIndex]):
            with open('./conversation/conv_blocks/' + pipeline[blockIndex].name + ".json", 'r') as f:
                block = json.load(f)
                return {"response": "Good and" + block["parameters"][paramIndex]["question"]}
        else:
            return "BUBUBUB"

    def hasParameters(self, block):
        if len(block.parameters) == 0 or not os.path.exists('./conversation/conv_blocks/' + block.name + '.json'):
            return False
        else:
            return True
