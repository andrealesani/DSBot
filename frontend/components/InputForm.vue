<template>
  <div>
    <v-card class="mb-12" height="300px">
      Upload your data
      <v-file-input truncate-length="15" v-model="dataset"></v-file-input>
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
      separator_list: [',', ';'],
      separator: ',',
      dataset: null,
    }
  },
  methods: {
    async sendData() {
      console.log(this.dataset)
      const formdata = new FormData()
      formdata.append('has_column_names', this.hasColumnNames)
      formdata.append('ds', this.dataset)
      formdata.append('has_index', this.hasIndex)
      formdata.append('separator', this.separator)
      formdata.append('format', '.csv')

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
