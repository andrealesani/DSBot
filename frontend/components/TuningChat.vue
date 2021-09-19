<template>
  <div>
    <v-card class="mr-10" width="400px" flat>
      Chat
      <div v-for="(item, index) in tuningChat" :key="index" class="pa-2">
        <v-card>
          {{ item }}
        </v-card>
      </div>
      <div>
        <v-row align="center">
          <v-text-field
            v-model="utterance"
            background-color="grey lighten-3"
          ></v-text-field>
          <v-spacer />
          <v-btn color="primary" @click="toFramework(utterance)"> Send </v-btn>
        </v-row>
      </div>
    </v-card>
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
