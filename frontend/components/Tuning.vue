<template>
  <div>
    <v-card class="mb-12 mt-3" flat>
      <v-row justify="center">
        <img
          :src="`data:image/png;base64,${imageBase64}`"
          alt=""
          height="500"
        />
        <tuning-chat />
        <v-col>
          <tuningBlock
            v-for="(item, i) in tuningPipeline"
            :key="i"
            :module="item"
          />
        </v-col>
      </v-row>
    </v-card>
  </div>
</template>

<script>
import { mapState } from 'vuex'
export default {
  data() {
    return {}
  },
  computed: {
    ...mapState(['imageBase64', 'tuningPipeline']),
  },
  methods: {},
}
</script>

<style scoped></style>
