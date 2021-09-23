<template>
  <v-card :color="module.is_highlighted ? '#FFF9BF' : 'white'" height="100%">
    <v-card-title>
      {{ module.pretty_name }}
    </v-card-title>

    <p v-if="module.parameters.length === 0" class="px-3">
      This operation doesn't contain any parameter
    </p>

    <tuning-parameter
      v-for="parameter in module.parameters"
      :key="parameter.name"
      :param="parameter"
      :module="module.name"
    />
  </v-card>
</template>

<script>
export default {
  props: ['module'],
}
</script>

<style scoped></style>
