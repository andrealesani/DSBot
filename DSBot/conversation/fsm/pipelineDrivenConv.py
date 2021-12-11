import json

from DSBot.conversation.fsm.json_helper import Json_helper


class pipelineDrivenConv:
    js = Json_helper()
    blockIndex = 0  # indice lista blocchetti da mettere nel json


    # stati-> (introduction,) parametersSetting, endBlock


    def __init__(self, session_id, pipeline):
        self.js.updatestate(session_id, "parametersSetting")
        self.pipeline = pipeline  # metti pipeline in dizionario
        self.param = 0 # metti in json indice parametro =0
        pass

        #danno errore, perché la pipeline non è serializzabile
        #self.js.addPipeline(session_id, pipeline)
        #self.js.setCurrentBlock(session_id, 0)
        #self.js.setParamIndex(session_id, 0)



    def conversationHandler(self, intent, entities, session_id):

        """if self.js.getstate(session_id) == "intro":
            if intent == "affirm":
                #TODO add detailed explanation in the json
                pass"""

        if self.js.getstate(session_id) == "parametersSetting":
            with open('./conversation/conv_blocks/' + self.pipeline[self.blockIndex].name + ".json", 'r') as f:
                block = json.load(f)
            if block["name"] == "kmeans":
                if intent == "clustering":
                    pass





    pass

        #check(intent, entities, stato)

        #----->set_parameter
        #modifica stato

        #if stato == fine
            # maximanager ->check

        #else send_response



    def maxiManager(self, session_id):
        # verifica che il blocchetto sia utile e che lo stato non sia fine blocchetto altrimetni prende  # quello dopo (fa anche il check dei parametri)
        #da aggiungere agglomerative variance treshold e outliers(?)

        if self.js.getstate(session_id) == "endBlock":
            self.blockIndex += 1
            self.param = 0
            self.js.updatestate(session_id, "parametersSetting")

        while(self.pipeline[self.blockIndex].name != "dbscan" and self.pipeline[self.blockIndex].name != "kmeans" and
                  self.pipeline[self.blockIndex].name != "laplace"):

            self.blockIndex += 1
            self.param = 0

            # send_introduction
        if (self.blockIndex < len(self.pipeline)):
            with open('./conversation/conv_blocks/' + self.pipeline[self.blockIndex].name + ".json", 'r') as f:
                block = json.load(f)
                toReturn = block["description"] +" " + block["parameters"][self.param]["question"]

            return toReturn
        else:
            pass



    def set_parameter(self):
        #modifica parametro pipeline
        pass









