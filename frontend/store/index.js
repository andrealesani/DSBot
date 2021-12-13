export const state = () => ({
  // Variable used by the v-stepper component to know which section of the webapp to show
  e1: 1,
  // Variable that is going to be filled with the sessionId
  sessionId: 1,
  // No idea
  requestDescription: '',
  // It becomes true when the backend has run the analysis and has sent the graph image
  resultsReady: false,
  // Graph that has to be shown, AKA results of the analysis
  imageBase64: null,
  // No idea
  resultsDetails: '',
  // Object used to store the chat messages and their sender. Initialized with welcome message
  tuningChat: [
    {
      isBot: true,
      message:
        'Welcome to Data Analysis Advisor! We can help you getting relevant information from your data. Don’t hesitate to ask for more explanation during every step of the conversation.',
    },
    {
      isBot: true,
      message: 'Would you like to do supervised or unsupervised learning?',
    },
  ],
  // Analysis pipeline used in the last section of the webapp to tune the hyperparameters
  tuningPipeline: [],
  // No idea why it's needed
  backendAvailable: true,
  // I guess it's used in the last section of the webapp
  pipelineEdited: false,
})

export const mutations = {
  setStep(state, newValue) {
    state.e1 = newValue
  },
  setSessionId(state, newId) {
    state.sessionId = newId
  },
  setRequestDescription(state, newRequest) {
    state.requestDescription = newRequest
  },
  setResultsReady(state, newState) {
    state.resultsReady = newState
  },
  setImage(state, image) {
    state.imageBase64 = image
  },
  setResultsDetails(state, details) {
    state.resultsDetails = details
  },
  sendChat(state, msg) {
    state.tuningChat.push({ isBot: false, message: msg })
  },
  removeWait(state) {
    state.tuningChat.pop()
    /* const chat = state.tuningChat
    for (const element in chat) {
      if (element.isBot && element.message === '#wait') {
        const deletedElement = state.tuningChat.splice(chat.indexOf(element), 1)
        if (deletedElement.len < 1) alert("couldn't deletedElement")
        else alert('element deleted')
      }
    } */
  },
  clearChat(state) {
    state.tuningChat = []
  },
  receiveChat(state, msg) {
    if (msg) state.tuningChat.push({ isBot: true, message: msg })
  },
  setTuningPipeline(state, pipeline) {
    state.tuningPipeline = pipeline
  },
  setAvailable(state, available) {
    state.backendAvailable = available
  },

  setPipelineEdited(state, edited) {
    state.pipelineEdited = edited
  },
}

export const actions = {
  async sendDataStore(context, inputData) {
    console.log('AAA', inputData)
    const formdata = new FormData()
    formdata.append('has_column_names', inputData.hasColumnNames)
    formdata.append('ds', inputData.ds)
    formdata.append('has_index', inputData.hasIndex)
    formdata.append('separator', inputData.separator)
    formdata.append('format', inputData.format)
    formdata.append('label', inputData.label)

    console.log('FormData')
    for (const value of formdata.values()) {
      console.log(value)
    }

    const res = await this.$axios
      .post('/receiveds', formdata, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })
      .then(function (response) {
        context.commit('setSessionId', response.data.session_id)
        context.commit('setStep', 2)
      })
      .catch(function (e) {
        console.log('FAILURE!!', e)
      })
    return res
  },

  async sendUtterance(context, sentence) {
    if (sentence === '') return null

    const bodyRequest = {
      session_id: this.state.sessionId,
      message: sentence,
    }
    console.log(bodyRequest)
    const res = await this.$axios
      .post('/utterance', bodyRequest)
      .then(function (response) {
        context.commit('setRequestDescription', response.data.request)
        context.commit('setStep', 3)
      })
    return res
  },

  async waitForResults(context) {
    console.log(
      'WAIT FOR RESULTS with sessionID ' + this.state.sessionId,
      this.state.e1
    )
    if (!this.state.resultsReady) {
      console.log('GET RESULTS CALLED')
      const pollingResponse = await this.$axios
        .get(`/results/${this.state.sessionId}`)
        .then(function (response) {
          console.log(response)
          if (response.data.ready) {
            context.commit('setImage', response.data.img)
            context.commit('setResultsDetails', response.data.details)
            context.commit('setResultsReady', response.data.ready)
            context.commit('receiveChat', response.data.tuning.utterance)
            context.commit('setPipelineEdited', false)
          } else {
            console.log('Non faccio niente')
          }
        })
      return pollingResponse
    }

    return null
  },

  async toFramework(context, data) {
    if (!this.state.backendAvailable) {
      return null
    }
    context.commit('setAvailable', false)

    const isUtterance = typeof data === 'string' || data instanceof String
    let bodyRequest
    if (isUtterance) {
      context.commit('sendChat', data)
      bodyRequest = {
        session_id: this.state.sessionId,
        type: 'utterance',
        utterance: data,
      }
    } else {
      bodyRequest = {
        session_id: this.state.sessionId,
        type: 'payload',
        payload: data,
      }
    }
    const res = await this.$axios
      .post('/tuning', bodyRequest)
      .then(function (response) {
        console.log(response)

        if ('utterance' in response.data.tuning) {
          context.commit('receiveChat', response.data.tuning.utterance)
        }
        if ('payload' in response.data.tuning) {
          if (response.data.tuning.payload.status === 'choose_problem') {
            // context.commit('setStep', 3) // Assume already in step 3 and can't come back from 4
            context.commit('setImage', response.data.tuning.payload.result)
          } else if (response.data.tuning.payload.status === 'edit_param') {
            context.commit('setStep', 4)
            context.commit(
              'setTuningPipeline',
              response.data.tuning.payload.pipeline
            )
          } else if (response.data.tuning.payload.status === 'end') {
            context.commit('setResultsReady', false)
            context.commit('setStep', 3)
          } else {
            console.log(
              'Unknown tuning status:',
              response.data.tuning.payload.status
            )
          }
        }

        context.commit('setAvailable', true)
      })
    return res
  },

  // Sends the message to the backend, then adds the user message to the chat panel, waits for server response and adds it to chat panel too
  async sendChatMessage(context, data) {
    // The data can be {destination: '/yourDestination', payload: userUtterance}

    // Add the message to the chat panel
    context.commit('sendChat', data.payload)

    // This is the data sent to the backend
    const bodyRequest = {
      session_id: this.state.sessionId,
      payload: data.payload,
    }
    const res = await this.$axios
      .post(data.destination, bodyRequest)
      .then(function (response) {
        // Adds the 3 dots to the chat panel
        context.commit('receiveChat', '#wait')
        setTimeout(() => {
          // Removes the 3 dots and adds the actual message to the chat panel
          context.commit('removeWait')
          context.commit('receiveChat', response.data.response)
          if (response.data.image !== null) {
            context.commit('setImage', response.data.image)
          }
        }, 1500)
      })
    return res
  },
  clearChat(context) {
    context.commit('clearChat')
  },
  async getHelp(context, data) {
    const bodyRequest = {
      session_id: this.state.sessionId,
    }

    const res = await this.$axios
      .post('/get-help', bodyRequest)
      .then(function (response) {
        if (response.data.image !== null) {
          context.commit('setImage', response.data.image)
        }
      })
    return res
  },
}
