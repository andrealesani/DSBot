<template>
  <div>
    <v-card class="mb-12" height="200px">
      Upload your data
      <v-file-input truncate-length="15"></v-file-input>
      <v-switch
        v-model="hasIndex"
        flat
        :label="`The file rows have ${hasKeys ? '' : 'not'} Keys`"
      ></v-switch>
      <v-switch
        v-model="hasColumnNames"
        flat
        :label="`The file rows have ${
          hasColumnNames ? '' : 'not'
        } column names`"
      ></v-switch>
    </v-card>
    <!-- <v-btn color="primary"> Continue </v-btn> -->
    <v-btn color="primary" @click="sendData"> ConAAAtinue </v-btn>
  </div>
</template>

<script>
export default {
  components: {},
  data() {
    return {
      e1: 1,
      hasIndex: true,
      hasColumnNames: true,
    }
  },
  methods: {
    async sendData() {
      const formdata = new FormData()
      formdata.append('has_column_names', this.hasColumnNames)
      formdata.append('has_index', this.hasIndex)

      const res = await this.$axios
        .post('/receiveds', formdata, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        })
        .then(function (response) {
          console.log(response.data)
        })
        .catch(function () {
          console.log('FAILURE!!')
        })
      return res
    },
  },
}
</script>
