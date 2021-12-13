<template>
  <v-row justify="center" align="center">
    <v-col cols="12" sm="12" md="12">
      <v-stepper v-model="e1">
        <v-stepper-header>
          <v-stepper-step :complete="e1 > 1" step="1">
            Upload your data
          </v-stepper-step>

          <v-divider></v-divider>

          <v-stepper-step :complete="e1 > 2" step="2">
            Explain your analysis
          </v-stepper-step>

          <v-divider></v-divider>

          <v-stepper-step :complete="e1 > 3" step="3">
            View your results
          </v-stepper-step>

          <v-divider></v-divider>

          <v-stepper-step :complete="e1 > 4" step="4">
            Tune your pipeline
          </v-stepper-step>
        </v-stepper-header>

        <v-stepper-items>
          <v-stepper-content step="1" class="px-10 pb-8">
            <input-form></input-form>
          </v-stepper-content>

          <v-stepper-content step="2" class="px-10 pb-8">
            <v-row>
              <v-col>
                <tuning-chat destination="/echo"></tuning-chat>
              </v-col>
              <v-col>
                <chat-helper></chat-helper>
              </v-col>
            </v-row>
          </v-stepper-content>

          <v-stepper-content step="3" class="px-10 pb-8">
            <results></results>

            <v-btn color="secondary" @click="restart()"> Restart </v-btn>
            <v-btn
              v-if="resultsReady"
              color="secondary"
              @click="toFramework({ intent: 'skip' })"
            >
              Continue without choosing a problem
            </v-btn>
          </v-stepper-content>

          <v-stepper-content step="4" class="px-10 pb-8">
            <tuning></tuning>

            <v-btn color="secondary" @click="restart()"> Restart </v-btn>
            <v-btn
              v-if="resultsReady"
              :color="pipelineEdited ? 'primary' : 'secondary'"
              @click="toFramework({ intent: 'run' })"
            >
              Run again
            </v-btn>
          </v-stepper-content>
        </v-stepper-items>
      </v-stepper>
    </v-col>
  </v-row>
</template>

<script>
import { mapState, mapMutations, mapActions } from 'vuex'

export default {
  data() {
    return {
      polling: null,
    }
  },
  computed: {
    ...mapState(['e1', 'resultsReady', 'pipelineEdited']),
  },
  mounted() {
    this.polling = setInterval(() => this.waitForResults(), 3000)
  },
  methods: {
    ...mapMutations(['setStep', 'setResultsReady', 'setAvailable']),
    ...mapActions(['toFramework', 'waitForResults']),
    restart() {
      this.setAvailable(true)
      this.setResultsReady(false)
      this.setStep(1)
    },
  },
}
</script>
