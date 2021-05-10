<template>
  <div>
    <v-card class="mb-12" height="200px">
      Upload your data
      <v-file-input truncate-length="15"></v-file-input>
      <v-switch
        v-model="has_keys"
        flat
        :label="`The file rows have ${has_keys ? '' : 'not'} Keys`"
      ></v-switch>
      <v-switch
        v-model="has_column_names"
        flat
        :label="`The file rows have ${
          has_column_names ? '' : 'not'
        } column names`"
      ></v-switch>
    </v-card>
    <!-- <v-btn color="primary"> Continue </v-btn> -->
    <!-- <v-btn color="primary" @click="e1 = 2"> Continue </v-btn> -->
  </div>
</template>

<script>
export default {
  components: {},
  data() {
    return {
      e1: 1,
      has_keys: true,
      has_column_names: true,
    }
  },
}
</script>
