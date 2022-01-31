export const state = () => ({
  // Variable used by the v-stepper component to know which section of the webapp to show
  e1: 1,
  // Variable that is going to be filled with the sessionId
  sessionId: 1,
  // No idea
  requestDescription: '',
  // It becomes true when the backend has run the analysis and has sent the graph image
  resultsReady: false,
  // Variable that stores an image received from the backend, for example the results of the analysis
  imageBase64: null,
  // No idea
  resultsDetails: '',
  // Object used to store the chat messages and their sender. Initialized with welcome message
  tuningChat: [
    {
      isBot: true,
      message:
        'Welcome to Data Analysis Advisor! 😁 We can help you getting relevant information from your data. Don’t hesitate to ask for more explanation during every step of the conversation.',
    },
    {
      isBot: true,
      message: 'Would you like to do supervised or unsupervised learning?',
    },
  ],
  // When true, chatHelper component shows the help message
  showHelp: true,
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
    state.showHelp = false
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
  setShowHelp(state, bool) {
    state.showHelp = bool
  },
  invertShowHelp(state) {
    state.showHelp = !state.showHelp
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
    if (this.state.e1 === 3 && !this.state.resultsReady) {
      console.log('CALLED /results/sessionId')
      const pollingResponse = await this.$axios
        .get(`/results/${this.state.sessionId}`)
        .then(function (response) {
          console.log(response)
          if (response.data.ready) {
            context.commit('setStep', 3)
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
        context.commit('receiveChat', '#wait')
        // Array of strings containing the messages sent by the bot
        const messagesArray = response.data.response
        // Typing speed of the bot (in milliseconds per character)
        const typingSpeed = 25
        // Maximum wait time for a message to be written
        const maxWaitTime = 3000
        // Minimum wait time for a message to be written
        const minWaitTime = 1500
        // Time to wait before starting to print the current message
        let totalTime = 0
        // Print the messages
        for (let i = 0; i < messagesArray.length; i++) {
          // Number of characters in the message
          const charSum = messagesArray[i].length
          // Actual typing speed of the bot. It inherits the value of 'typingSpeed' for long messages, but it's overwritten for short messages
          let actualSpeed
          // It slows down the typing speed if the message is too short and would be sent too quickly
          if (messagesArray[i].length * typingSpeed < minWaitTime) {
            actualSpeed = 1500 / charSum
          }
          // It caps the maximum time for a message to be sent to 3 seconds
          else if (messagesArray[i].length * typingSpeed > maxWaitTime) {
            actualSpeed = 3000 / charSum
          } else {
            actualSpeed = typingSpeed
          }
          setTimeout(() => {
            // Removes the 3 dots
            context.commit('removeWait')
            // Adds the actual message to the chat panel
            context.commit('receiveChat', messagesArray[i])
            // Adds the 3 dots to the chat panel for the next message (it doesn't add them if it's the last message)
            if (i < messagesArray.length - 1) {
              context.commit('receiveChat', '#wait')
            }
            // Go to loading screen if the analysis has started
            if (
              messagesArray[i] ===
              'Ok, parameter tuning is completed, in a moment you will see the results'
            ) {
              context.commit('setStep', 3)
            }
          }, totalTime + charSum * actualSpeed)
          console.log(messagesArray[i])
          console.log('took ' + charSum * actualSpeed + 'ms to be printed')
          totalTime += charSum * actualSpeed
        }

        // If there is an image attached to the message show it inside ChatHelper component
        if (response.data.image !== null && response.data.image !== undefined) {
          context.commit('setImage', response.data.image)
        }
      })
    return res
  },

  // Clears the chat array
  clearChat(context) {
    context.commit('clearChat')
  },
  getHelp(context) {
    if (this.state.e1 !== 2) {
      alert('Help button is only available in step 2')
      return
    }
    context.commit('invertShowHelp')
  },
}
