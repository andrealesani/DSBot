<template>
  <div>
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
  </div>
</template>

<script>
import { mapActions, mapState } from 'vuex'
export default {
  components: {},
  data() {
    return {
      polling: null,
    }
  },
  computed: {
    ...mapState(['resultsReady', 'imageBase64']),
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
    this.pollData()
  },
}
</script>

<style scoped></style>
