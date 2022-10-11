<template>
  <div>
    <v-card class="mb-12" height="140px" flat>
      What you want to obtain?
      <v-textarea
        v-model="utterance"
        background-color="grey lighten-3"
      ></v-textarea>
    </v-card>
    <!-- <v-btn color="primary"> Continue </v-btn> -->
    <v-btn color="primary" @click="sendUtterance(utterance)"> Continue </v-btn>
    <v-btn color="primary" @click="clearChat()"> Clear chat </v-btn>
  </div>
</template>

<script>
import { mapActions } from 'vuex'

export default {
  components: {},
  data() {
    return {
      utterance: '',
    }
  },
  methods: {
    ...mapActions(['sendUtterance', 'clearChat']),
  },
}
</script>
