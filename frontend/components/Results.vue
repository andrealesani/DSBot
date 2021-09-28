<template>
  <div>
    <v-card class="mb-5" flat>
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
      <results-row v-if="resultsReady" />
    </v-card>
  </div>
</template>

<script>
import { mapState } from 'vuex'
export default {
  computed: {
    ...mapState(['resultsReady']),
  },
}
</script>

<style scoped></style>
