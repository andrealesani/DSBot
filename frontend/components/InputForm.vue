<template>
  <div>
    <v-card class="mb-12" height="300px" flat>
      <v-file-input
        v-model="dataset"
        color="secondary"
        truncate-length="15"
        :error="fileInputError"
        label="select a CSV"
      ></v-file-input>
      <!-- <v-layout row wrap justify-center> -->
      <!-- <v-flex xs5> -->
      <v-switch
        v-model="hasIndex"
        flat
        color="secondary"
        :label="`The file rows have ${hasIndex ? '' : 'not'} Keys`"
      ></v-switch>
      <!-- </v-flex> -->
      <!-- <v-flex xs6> -->
      <v-switch
        v-model="hasColumnNames"
        flat
        color="secondary"
        :label="`The file rows have ${
          hasColumnNames ? '' : 'not'
        } column names`"
      ></v-switch>
      <!-- </v-flex> -->
      <!-- </v-layout> -->
      <v-flex xs5>
        <v-select
          v-model="separator"
          color="secondary"
          :items="separator_list"
          :error="separatorError"
          label="Separator"
        ></v-select>
      </v-flex>
      <v-flex xs7>
        <v-text-field
          v-model="label"
          color="secondary"
          label="Label (leave blank if not present)"
        ></v-text-field>
      </v-flex>
    </v-card>
    <!-- <v-btn color="primary"> Continue </v-btn> -->
    <v-btn color="secondary" @click="sendData"> Continue </v-btn>
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
      separator: '',
      dataset: null,
      fileInputError: false,
      separatorError: false,
      fileInputHint: '',
      label: '',
    }
  },
  methods: {
    sendData() {
      this.fileInputError = !this.dataset
      this.separatorError = !this.separator
      if (!this.fileInputError && !this.separatorError) {
        this.fileInputError = false
        this.separatorError = false
        const inputData = {
          ds: this.dataset,
          hasColumnNames: this.hasColumnNames,
          hasIndex: this.hasIndex,
          separator: this.separator,
          format: '.csv',
          label: this.label,
        }
        this.sendDataStore(inputData)
      }
    },
    ...mapActions(['setStep', 'sendDataStore']),
  },
  actions: {},
}
</script>
