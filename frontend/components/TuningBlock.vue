<template>
  <div>
    <v-card class="mb-12" height="250px" width="300px">
      <v-card-title>
        <h2>{{ module.pretty_name }}</h2>
      </v-card-title>
      <component
        v-for="parameter in module.parameters"
        :is="
          parameter.type === 'float' || parameter.type === 'int'
            ? 'tuning-slider'
            : 'tuning-radio'
        "
        :key="parameter.name"
        :param="parameter"
        :module="module.name"
      ></component>
    </v-card>
  </div>
</template>

<script>
export default {
  props: ['module'],
}
</script>

<style scoped></style>
