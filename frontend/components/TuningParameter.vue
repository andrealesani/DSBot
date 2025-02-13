<template>
  <div>
    <v-col>
      <v-tooltip bottom>
        <template #activator="{ on, attrs }">
          <span v-bind="attrs" v-on="on">{{ param.pretty_name }}</span>
        </template>
        <span>{{ param.description }}</span>
      </v-tooltip>

      <div v-if="isVisible">
        <v-slider
          v-if="isSlider"
          :key="param.name"
          v-model="localValue"
          hide-details
          :min="param.min"
          :max="param.max"
          :color="param.is_highlighted ? 'red' : 'secondary'"
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

        <v-select
          v-if="isCategorical"
          :key="param.name"
          v-model="localValue"
          :items="param.possible_val"
          hide-details
          :background-color="
            param.is_highlighted
              ? 'orange'
              : module.is_highlighted
              ? '#FFF9BF'
              : 'white'
          "
          :prepend-icon="param.value === param.default ? '' : 'mdi-restore'"
          @click:prepend="reset"
          ><template #append>
            <v-progress-circular
              v-if="coolingDown"
              indeterminate
              color="gray"
              size="15"
              width="2"
            /> </template
        ></v-select>
      </div>
      <div v-else class="px-3">This parameter is not enabled</div>
    </v-col>
  </div>
</template>

<script>
import { mapActions, mapMutations } from 'vuex'
export default {
  props: ['param', 'module'],
  data() {
    const iSl = this.param.type === 'float' || this.param.type === 'int'
    const iCa = this.param.type === 'categorical'

    return {
      cooldown: null,
      coolingDown: false,
      isSlider: iSl,
      isCategorical: iCa,
      isVisible:
        (iSl && this.param.max !== this.param.min) ||
        (iCa && this.param.possible_val.length > 1),
    }
  },
  computed: {
    localValue: {
      get() {
        return this.param.value
      },
      set(val) {
        this.setPipelineEdited(true)
        if (this.coolingDown) clearTimeout(this.cooldown)
        this.coolingDown = true
        this.cooldown = setTimeout(
          () => {
            this.coolingDown = false
            this.toFramework({
              intent: 'set',
              module: this.module.name,
              parameter: this.param.name,
              value: val,
            })
          },
          this.isSlider ? 2000 : 100 // Different cooling down duration
        )
      },
    },
  },
  methods: {
    ...mapActions(['toFramework']),
    reset() {
      this.toFramework({
        intent: 'reset',
        module: this.module.name,
        parameter: this.param.name,
      })
    },
    ...mapMutations(['setPipelineEdited']),
  },
}
</script>

<style scoped></style>
