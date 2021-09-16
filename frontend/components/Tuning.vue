<template>
  <div>
    <TuningBlock v-for="(item, i) in tuningPipeline" :key="i" :module="item" />
  </div>
</template>

<script>
import { mapState } from 'vuex'
import TuningBlock from './TuningBlock.vue'
export default {
  components: { TuningBlock },
  data() {
    return {}
  },
  computed: {
    ...mapState(['tuningPipeline']),
  },
  methods: {},
}
</script>

<style scoped></style>
