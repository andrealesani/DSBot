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
import { mapState } from 'vuex'
export default {
  components: {},
  data() {
    return {
      imgWidth: 8,
    }
  },
  computed: {
    ...mapState(['resultsReady', 'imageBase64']),
  },
}
</script>

<style scoped></style>
