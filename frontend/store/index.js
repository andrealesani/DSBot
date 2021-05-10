export const state = () => ({
  e1: 1,
  sessionId: 0,
  operationsArray: [
    {
      operation_id: 0,
      request:
        'operation -> operation -> operation -> operation  -> operation -> operation ',
    },
    {
      operation_id: 1,
      request:
        'long operation -> long operation -> long operation -> long operation  -> long operation -> long operation',
    },
  ],
})

export const mutations = {
  setStep(state, newValue) {
    state.e1 = newValue
  },
}

export const actions = {}
