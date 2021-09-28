<template>
  <div>
    <v-card class="mb-12" flat>
      <results-row />
      <v-row>
        <v-col v-for="(item, i) in tuningPipeline" :key="i" :cols="4">
          <tuningBlock :module="item" />
        </v-col>
      </v-row>
    </v-card>
  </div>
</template>

<script>
import { mapState } from 'vuex'
export default {
  computed: {
    ...mapState(['tuningPipeline']),
  },
}
</script>

<style scoped></style>
