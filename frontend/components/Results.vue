<template>
  <div>
    <v-card height="500px" flat>
      <div v-if="!resultsReady" class="text-center">
        <div>
          <v-progress-circular
            indeterminate
            color="success"
            size="100"
            width="10"
          />
        </div>
        We are performing your analysis
        <v-btn color="warning" @click="pollData"> Manual poll </v-btn>
      </div>
      <v-row v-if="resultsReady" justify="center">
        <v-col :cols="imgWidth">
          <img
            :src="`data:image/png;base64,${imageBase64}`"
            alt=""
            height="500"
          />
        </v-col>
        <v-col :cols="12 - imgWidth">
          <tuning-chat />
        </v-col>
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
      imgWidth: 8,
    }
  },
  computed: {
    ...mapState(['resultsReady', 'imageBase64']),
  },
  mounted() {
    console.log('Results mounted!') // TODO: how to call it a second time?
    this.pollData()
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
}
</script>

<style scoped></style>
