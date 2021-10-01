<template>
  <div>
    <v-col>
      <v-tooltip bottom>
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
          :color="param.is_highlighted ? 'primary' : 'secondary'"
          :track-color="'secondary'"
          :thumb-label="true"
          :step="param.type === 'int' ? '1' : '0.1'"
          :prepend-icon="param.value === param.default ? '' : 'mdi-restore'"
          @click:prepend="reset"
        >
          <template #append>
            {{ coolingDown ? '' : localValue }}
            <v-progress-circular
              v-if="coolingDown"
              indeterminate
              color="gray"
              size="15"
              width="2"
            />
          </template>
        </v-slider>
      </div>
    </v-col>
  </div>
</template>

<script>
import { mapActions } from 'vuex'
export default {
  props: ['param', 'module'],
  data() {
    return {
      cooldown: null,
      coolingDown: false,
      isSlider: this.param.type === 'float' || this.param.type === 'int',
    }
  },
  computed: {
    localValue: {
      get() {
        return this.param.value
      },
      set(val) {
        if (this.coolingDown) clearTimeout(this.cooldown)
        this.coolingDown = true
        this.cooldown = setTimeout(() => {
          this.coolingDown = false
          this.toFramework({
            intent: 'set',
            module: this.module,
            parameter: this.param.name,
            value: val,
          })
        }, 2000)
      },
    },
  },
  methods: {
    ...mapActions(['toFramework']),
    reset() {
      this.toFramework({
        intent: 'reset',
        module: this.module,
        parameter: this.param.name,
      })
    },
  },
}
</script>

<style scoped></style>
