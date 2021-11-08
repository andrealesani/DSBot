<template>
  <v-card :color="module.is_highlighted ? '#FFF9BF' : 'white'" height="100%">
    <v-card-title>
      <v-select
        v-if="available.length > 1"
        v-model="activeMod"
        :items="available"
        solo
        flat
        hide-details
        :background-color="
          module.should_change
            ? 'orange'
            : module.is_highlighted
            ? '#FFF9BF'
            : 'white'
        "
        :append-icon="'mdi-menu'"
      ></v-select>
      <div v-else>
        {{ module.pretty_name }}
      </div>
    </v-card-title>

    <p v-if="module.parameters.length === 0" class="px-3">
      This operation doesn't contain any parameter
    </p>

    <tuning-parameter
      v-for="parameter in module.parameters"
      :key="parameter.name"
      :param="parameter"
      :module="module"
    />
  </v-card>
</template>

<script>
import { mapActions, mapMutations } from 'vuex'
export default {
  props: ['module'],

  computed: {
    available: {
      get() {
        return this.module.models.map((i) => i.pretty_name)
      },
    },
    activeMod: {
      get() {
        return this.module.pretty_name
      },
      set(val) {
        this.setPipelineEdited(true)
        this.toFramework({
          intent: 'set_module',
          module: this.module.name,
          value: val,
        })
      },
    },
  },
  methods: {
    ...mapActions(['toFramework']),
    ...mapMutations(['setPipelineEdited']),
  },
}
</script>

<style scoped></style>
