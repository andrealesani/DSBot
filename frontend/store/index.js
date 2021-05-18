export const state = () => ({
  e1: 3,
  sessionId: 1,
  requestDescription: '',
  resultsReady: false,
  imageBase64: null,
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
    if (!this.state.resultsReady) {
      const pollingResponse = await this.$axios
        .get(`/results/${this.state.sessionId}`)
        .then(function (response) {
          console.log(response)
          context.commit('setImage', response.data.img)
          context.commit('setResultsReady', response.data.ready)
        })
      return pollingResponse
    }

    return null
  },
}
