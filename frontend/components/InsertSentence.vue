<template>
  <div>
    <v-card class="mb-12" height="100px" flat>
      What you want to obtain?
      <v-textarea v-model="utterance" height="100px"></v-textarea>
    </v-card>
    <!-- <v-btn color="primary"> Continue </v-btn> -->
    <v-btn color="primary" @click="sendUtterance(utterance)"> Continue </v-btn>
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
    ...mapActions(['sendUtterance']),
  },
}
</script>
