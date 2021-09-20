<template>
  <div>
    <v-col>
      <v-tooltip right>
        <template #activator="{ on, attrs }">
          <span v-bind="attrs" v-on="on">{{ param.pretty_name }}</span>
        </template>
        <span>{{ param.description }}</span>
      </v-tooltip>
      <div v-if="isSlider">
        <v-slider
          :key="param.name"
          v-model="localValue"
          :min="param.min"
          :max="param.max"
          :color="param.is_highlighted ? 'red' : '#1875D1'"
          :track-color="'#434343'"
        >
          <template #append>
            <v-text-field
              v-model="localValue"
              class="mt-0 pt-0"
              hide-details
              single-line
              type="number"
              style="width: 60px"
            ></v-text-field>
          </template>
        </v-slider>
      </div>
    </v-col>
  </div>
</template>

<script>
export default {
  // parameter.type === 'float' || parameter.type === 'int'

  props: ['param', 'module'],
  data() {
    return {
      sliderValue: this.param.value,
      isSlider: this.param.type === 'float' || this.param.type === 'int',
      color: 'red',
    }
  },
  computed: {
    localValue: {
      get() {
        return this.param.value
      },
      set(value) {
        // TODO: Mandarlo al backend
      },
    },
  },
  mounted() {
    console.log('MOUNED', this.module)
  },
}
</script>

<style scoped></style>
