<template>
  <v-row justify="center" align="center">
    <v-col cols="12" sm="8" md="9">
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

          <v-stepper-step step="3"> Results</v-stepper-step>
        </v-stepper-header>

        <v-stepper-items>
          <v-stepper-content step="1">
            <input-form></input-form>

            <v-btn color="primary" @click="e1 = 2"> Continue </v-btn>

            <v-btn text> Cancel </v-btn>
          </v-stepper-content>

          <v-stepper-content step="2">
            <v-card class="mb-12" height="200px">
              What you want to obtain?
              <v-textarea></v-textarea>
            </v-card>

            <v-btn color="primary" @click="e1 = 3"> Continue </v-btn>

            <v-btn text> Cancel </v-btn>
          </v-stepper-content>

          <v-stepper-content step="3">
            <v-card class="mb-12" height="200px"> Here the results! </v-card>

            <v-btn color="primary" @click="e1 = 1"> Continue </v-btn>

            <v-btn text> Cancel </v-btn>
          </v-stepper-content>
        </v-stepper-items>
      </v-stepper>
    </v-col>
  </v-row>
</template>

<script>
import InputForm from '~/components/InputForm'

export default {
  components: {
    InputForm,
  },
  data() {
    return {
      e1: 1,
    }
  },
}
</script>
