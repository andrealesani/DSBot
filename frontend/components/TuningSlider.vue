<template>
  <div>
    <v-col>
      <v-tooltip right>
        <template v-slot:activator="{ on, attrs }">
          <span v-bind="attrs" v-on="on">{{ param.pretty_name }}</span>
        </template>
        <span>{{ param.description }}</span>
      </v-tooltip>
      <v-slider
        :min="param.min"
        :max="param.max"
        :key="param.name"
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
        </template> </v-slider
    ></v-col>
  </div>
</template>

<script>
export default {
  props: ['param', 'module'],
  data() {
    return {
      sliderValue: this.param.value,
    }
  },
  mounted() {
    console.log('MOUNED', this.module)
  },
}
</script>

<style scoped></style>
