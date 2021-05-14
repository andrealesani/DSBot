<template>
  <div>
    <v-card class="mb-12" height="300px">
      Upload your data
      <v-file-input
        v-model="dataset"
        truncate-length="15"
        :error="fileInputError"
        label="select a CSV"
      ></v-file-input>
      <v-switch
        v-model="hasIndex"
        flat
        :label="`The file rows have ${hasIndex ? '' : 'not'} Keys`"
      ></v-switch>
      <v-switch
        v-model="hasColumnNames"
        flat
        :label="`The file rows have ${
          hasColumnNames ? '' : 'not'
        } column names`"
      ></v-switch>
      <v-select
        v-model="separator"
        :items="separator_list"
        label="Separator"
      ></v-select>
    </v-card>
    <!-- <v-btn color="primary"> Continue </v-btn> -->
    <v-btn color="primary" @click="sendData"> Continue </v-btn>
  </div>
</template>

<script>
import { mapActions } from 'vuex'

export default {
  components: {},
  data() {
    return {
      hasIndex: true,
      hasColumnNames: true,
      separator_list: [',', ';'],
      separator: ',',
      dataset: null,
      fileInputError: false,
      fileInputHint: '',
    }
  },
  methods: {
    sendData() {
      if (this.dataset) {
        this.fileInputError = false
        const inputData = {
          ds: this.dataset,
          hasColumnNames: this.hasColumnNames,
          hasIndex: this.hasIndex,
          separator: this.separator,
          format: '.csv',
        }
        this.sendDataStore(inputData)
      } else {
        this.fileInputError = true
      }
    },
    ...mapActions(['setStep', 'sendDataStore']),
  },
  actions: {},
}
</script>
