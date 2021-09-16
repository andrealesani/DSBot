<template>
  <div>
    <v-card class="mb-12 mt-3" height="500px" flat>
      Chat
      <div v-for="item in tuningChat" :key="item">{{ item }}</div>
      <v-textarea
        v-model="utterance"
        background-color="grey lighten-3"
      ></v-textarea>
    </v-card>
    <v-btn color="primary" @click="toFramework(true, utterance)"> Send </v-btn>
  </div>
</template>

<script>
import { mapActions, mapState } from 'vuex'
export default {
  components: {},
  data() {
    return {
      utterance: '',
    }
  },
  computed: {
    ...mapState(['tuningChat']),
  },
  methods: {
    ...mapActions(['toFramework']),
  },
}
</script>

<style scoped></style>
