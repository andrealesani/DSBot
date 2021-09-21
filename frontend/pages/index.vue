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
            <insert-sentence></insert-sentence>
          </v-stepper-content>

          <v-stepper-content step="3" class="px-10 pb-8">
            <results></results>

            <v-btn color="secondary" @click="setStep(1)"> Restart </v-btn>
            <v-btn color="secondary" @click="toFramework({ intent: 'skip' })">
              Continue without choosing a problem
            </v-btn>
          </v-stepper-content>

          <v-stepper-content step="4" class="px-10 pb-8">
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

export default {
  computed: {
    ...mapState(['e1']),
  },
  methods: {
    ...mapMutations(['setStep']),
    ...mapActions(['toFramework']),
  },
}
</script>
