import json
import os

from DSBot.conversation.fsm.json_helper import Json_helper


# TODO declare as constants frequently used string or file paths such as:
#  "Ok, parameter tuning is completed, in a moment you will see the results", './conversation/conv_blocks/'
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
        self.js.setParamIndex(session_id, 0)
        self.js.setBlockIndex(session_id, 0)
        # self.param = 0  # metti in json indice parametro =0

    def conversationHandler(self, intent, entity, session_id):
        # retrieve current user's conversation state
        pipeline = self.pipelines[session_id]
        blockIndex = self.js.getBlockIndex(session_id)
        paramIndex = self.js.getParamIndex(session_id)

        """if self.js.getstate(session_id) == "intro":
            if intent == "affirm":
                #TODO add detailed explanation in the json
                pass"""

        if intent == "help":
            # TODO uniforma formato getBlockHelp e getHelp
            help = self.js.getBlockHelp(pipeline[blockIndex].name, paramIndex)
            return {"response": help}
        elif self.js.getstate(session_id) == "parametersSetting":
            # get current block
            with open('./conversation/conv_blocks/' + pipeline[blockIndex].name + ".json", 'r') as f:
                block = json.load(f)
            # update parameter with the user's choice (number)
            # TODO modify to set categorical parameters
            try:
                pipeline[blockIndex].parameters[block["parameters"][paramIndex]["name"]].tune_value(
                    int(entity))
            except:
                # invalid user input
                return {"response": ["Sorry, I didn't understand"]}
            # check: no more parameters to set for current block
            if paramIndex == (len(block["parameters"]) - 1):
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

    # verifica che il blocchetto sia utile e che lo stato non sia fine blocchetto altrimenti, prende quello
    # dopo (fa anche il check dei parametri); da aggiungere agglomerative, variance threshold e outliers(?)
    def maxiManager(self, session_id):

        # retrieve current user's conversation state
        pipeline = self.pipelines[session_id]
        blockIndex = self.js.getBlockIndex(session_id)
        paramIndex = self.js.getParamIndex(session_id)

        if self.js.getstate(session_id) == "endBlock" or blockIndex == 0:
            # TODO non ho capito perché si fa blockIndex+=1 se blockIndex==0, non si salta il primo block così?
            blockIndex += 1
            # self.js.setBlockIndex(session_id, blockIndex)
            # self.js.setParamIndex(session_id, 0)
            self.js.updatestate(session_id, "parametersSetting")
            # find next block with parameters to set
            try:
                while not self.hasParameters(pipeline[blockIndex]):
                    blockIndex += 1
            except IndexError:
                return {"response": ["Ok, parameter tuning is completed, in a moment you will see the results"]}
            self.js.setBlockIndex(session_id, blockIndex)
            self.js.setParamIndex(session_id, 0)

            # send introduction
            if (blockIndex < len(pipeline)):
                with open('./conversation/conv_blocks/' + pipeline[blockIndex].name + ".json", 'r') as f:
                    block = json.load(f)
                    toReturn = block["description"]
                    for s in block["parameters"][paramIndex]["question"]:
                        toReturn.append(s)
                return {"response": toReturn}
            else:
                return {"response": ["Ok, parameter tuning is completed, in a moment you will see the results"]}
        elif self.hasParameters(pipeline[blockIndex]):
            with open('./conversation/conv_blocks/' + pipeline[blockIndex].name + ".json", 'r') as f:
                block = json.load(f)
                return {"response": ["Good! And" + block["parameters"][paramIndex]["question"]]}
        else:
            return "Should not be her MAXIMANAGER line 117"

    def hasParameters(self, block):
        if len(block.parameters) == 0 or not os.path.exists('./conversation/conv_blocks/' + block.name + '.json'):
            return False
        else:
            return True
