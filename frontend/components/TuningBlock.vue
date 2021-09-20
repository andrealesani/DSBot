<template>
  <div>
    <v-card class="mb-12" height="250px" width="300px">
      <v-card-title>
        <h2>{{ module.pretty_name }}</h2>
      </v-card-title>
      <component
        v-for="parameter in module.parameters"
        :is="parameter.type === 'float' ? 'v-slider' : 'v-radio'"
        :min="parameter.min"
        :max="parameter.max"
        :key="parameter.name"
        v-model="sliderValue"
      >
        <template v-slot:append>
          <v-text-field
            v-model="sliderValue"
            class="mt-0 pt-0"
            hide-details
            single-line
            type="number"
            style="width: 60px"
          ></v-text-field>
        </template>
      </component>
    </v-card>
  </div>
</template>

<script>
export default {
  props: ['module'],
  data() {
    return {
      sliderValue: 0,
    }
  },
  mounted() {
    console.log('MOUNED', this.module)
  },
}
</script>

<style scoped></style>
