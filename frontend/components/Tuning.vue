<template>
  <div>
    <v-card class="mb-12" flat>
      <v-row justify="center">
        <v-col :cols="8">
          <img
            :src="`data:image/png;base64,${imageBase64}`"
            alt=""
            height="500"
          />
        </v-col>
        <v-col :cols="4">
          <tuning-chat />
        </v-col>
      </v-row>
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
    ...mapState(['imageBase64', 'tuningPipeline']),
  },
}
</script>
<style scoped></style>
