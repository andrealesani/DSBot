from conversation.fsm.json_helper import Json_helper


class pipelineDrivenConv:
    js = Json_helper()
    # stato dentro blocchetto o fine blocchetto-> intro, par_setting, fine
    # indice lista blocchetti
    # indice parametro

    def __init__(self, session_id, pipeline):
        pass
        # metti pipeline dentro json
        # metti in json stato = intro
        # metti in json indice parametro =0
        #maximanager


        #danno errore, perché la pipeline non è serializzabile
        #self.js.addPipeline(session_id, pipeline)
        #self.js.setCurrentBlock(session_id, 0)
        #self.js.setParamIndex(session_id, 0)

    def conversationHandler(self, intent, entities, session_id):
        pass
        #check(intent, entities, stato)

        #----->set_parameter
        #modifica stato

        #if stato == fine
            # maximanager ->check

        #else send_response



    def maxiManager(self):
        pass
        # verifica che il blocchetto sia utile e che lo stato non sia fine blocchetto altrimetni prende
        # quello dopo (fa anche il check dei parametri)
        #send_introduction



    #def set parameter
        #modifica parametro pipeline









