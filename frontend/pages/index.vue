<template>
  <v-row justify="center" align="center">
    <v-col cols="12" sm="8" md="8">
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

          <v-stepper-step :complete="e1 > 3" step="3"> Results</v-stepper-step>

          <v-divider></v-divider>

          <v-stepper-step step="4"> Tuning</v-stepper-step>
        </v-stepper-header>

        <v-stepper-items>
          <v-stepper-content step="1" class="px-10">
            <input-form></input-form>
          </v-stepper-content>

          <v-stepper-content step="2" class="px-10">
            <insert-sentence></insert-sentence>
          </v-stepper-content>

          <v-stepper-content step="3" class="px-10">
            <results></results>

            <v-btn color="secondary" @click="setStep(1)"> Restart </v-btn>
            <v-btn color="secondary" @click="toFramework({ intent: 'skip' })">
              Skip
            </v-btn>
          </v-stepper-content>

          <v-stepper-content step="4" class="px-10">
            <tuning></tuning>

            <v-btn color="secondary" @click="setStep(1)"> Restart </v-btn>
            <v-btn color="secondary" @click="toFramework({ intent: 'run' })">
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

import InputForm from '~/components/InputForm'
import InsertSentence from '~/components/InsertSentence'
import Results from '~/components/Results'
import Tuning from '~/components/Tuning'

export default {
  components: {
    InputForm,
    InsertSentence,
    Results,
    Tuning,
  },
  data() {
    return {
      // e1: 1,
    }
  },
  methods: {
    ...mapMutations(['setStep']),
    ...mapActions(['toFramework']),
  },
  computed: {
    ...mapState(['e1']),
  },
}
</script>
