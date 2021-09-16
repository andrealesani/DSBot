<template>
  <div>
    <v-col>
      <v-row>
        <v-card class="mb-12 mt-3" height="500px" flat>
          <div v-if="!resultsReady" class="text-center">
            <div>
              <v-progress-circular
                indeterminate
                color="green"
                size="100"
                width="10"
              ></v-progress-circular>
            </div>
            We are performing your analysis
          </div>
          <v-row justify="center">
            <img
              :src="`data:image/png;base64,${imageBase64}`"
              alt=""
              v-if="resultsReady"
              height="500"
            />
          </v-row>
        </v-card>
        <tuning-chat v-if="resultsReady" />
      </v-row>
      <Tuning v-if="resultsReady" />
    </v-col>
  </div>
</template>

<script>
import { mapActions, mapState } from 'vuex'
import TuningChat from './TuningChat.vue'
import Tuning from './Tuning.vue'
export default {
  components: { TuningChat, Tuning },
  data() {
    return {
      polling: null,
    }
  },
  computed: {
    ...mapState(['resultsReady', 'imageBase64', 'tuningChat']),
  },
  methods: {
    ...mapActions(['waitForResults']),
    pollData() {
      this.polling = setInterval(() => {
        if (!this.resultsReady) this.waitForResults()
        else clearInterval(this.polling)
      }, 3000)
    },
  },
  mounted() {
    console.log('Results mounted!')
    this.pollData()
  },
}
</script>

<style scoped></style>
