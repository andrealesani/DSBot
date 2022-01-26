<template>
  <v-row justify="center">
    <v-col :cols="3" :xl="5">
      <tuning-chat />
    </v-col>
    <v-col :cols="9" :xl="7">
      <img :src="`data:image/png;base64,${imageBase64}`" alt="" height="700" />
    </v-col>
    <v-col v-if="resultsDetails !== ''">
      <v-card class="mx-2 pa-2">
        <v-card-title>Pipeline execution details:</v-card-title>
        {{ resultsDetails }}
      </v-card>
    </v-col>
  </v-row>
</template>

<script>
import { mapState } from 'vuex'
export default {
  computed: {
    ...mapState(['imageBase64', 'resultsDetails']),
  },
}
</script>
<style scoped></style>
