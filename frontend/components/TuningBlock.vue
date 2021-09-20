<template>
  <div>
    <v-card
      class="mb-12"
      height="250px"
      width="300px"
      :color="module.is_highlighted ? '#f9c74f' : '#FFF'"
    >
      <v-card-title>
        <h2>{{ module.pretty_name }}</h2>
      </v-card-title>
      <tuning-parameter
        v-for="parameter in module.parameters"
        :key="parameter.name"
        :param="parameter"
        :module="module.name"
      ></tuning-parameter>
    </v-card>
  </div>
</template>

<script>
import TuningParameter from './TuningParameter.vue'
export default {
  components: { TuningParameter },
  props: ['module'],
}
</script>

<style scoped></style>
