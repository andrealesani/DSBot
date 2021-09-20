<template>
  <div>
    <v-card class="mb-12 mt-5" flat id="vcard">
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
    <button @click="setP">Button!</button>
  </div>
</template>

<script>
import { mapState, mapMutations } from 'vuex'
export default {
  data() {
    return {}
  },
  computed: {
    ...mapState(['imageBase64', 'tuningPipeline']),
  },
  methods: {
    setP() {
      this.setTuningPipeline([
        {
          name: 'pca2',
          pretty_name: 'PCA 2',
          is_highlighted: false,
          parameters: [
            {
              name: 'n_components',
              pretty_name: 'Number of components',
              value: 0,
              min: 0,
              max: 10,
              default: 2,
              description: 'Defines the number of components to keep.',
              is_highlighted: false,
              type: 'float',
            },
          ],
        },
      ])
    },
    ...mapMutations(['setTuningPipeline']),
  },
  mounted() {
    console.log('MOUNED', this.tuningPipeline)
  },
}
</script>
<style scoped></style>
