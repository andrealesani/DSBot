import { pipelineJson } from '~/test/pipeline-json'

export const state = () => ({
  e1: 3,
  sessionId: 1,
  requestDescription: '',
  resultsReady: false,
  imageBase64: null,
  tuningChat: [],
  tuningPipeline: pipelineJson,
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
  sendChat(state, msg) {
    state.tuningChat.push({ isBot: false, message: msg })
  },
  receiveChat(state, msg) {
    state.tuningChat.push({ isBot: true, message: msg })
  },
  setTuningPipeline(state, pipeline) {
    state.tuningPipeline = pipeline
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
    console.log('WAIT FOR RESULTS', this.state.e1)
    if (!this.state.resultsReady && this.state.e1 === 3) {
      console.log('GET RESULTS CALLED')
      const pollingResponse = await this.$axios
        .get(`/results/${this.state.sessionId}`)
        .then(function (response) {
          console.log(response)
          if (response.data.ready) {
            context.commit('setImage', response.data.img)
            context.commit('setResultsReady', response.data.ready)
            context.commit('receiveChat', response.data.tuning.utterance)
          } else {
            console.log('Non faccio niente')
          }
        })
      return pollingResponse
    }

    return null
  },

  async toFramework(context, data) {
    const isUtterance = typeof data === 'string' || data instanceof String
    console.log('SENDING DATA', isUtterance, data)
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
    console.log(bodyRequest)
    const res = await this.$axios
      .post('/tuning', bodyRequest)
      .then(function (response) {
        console.log('RECEIVED TUNING', response.data.tuning)
        if ('utterance' in response.data.tuning) {
          console.log(response.data.tuning.utterance)
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
      })
    return res
  },
}
