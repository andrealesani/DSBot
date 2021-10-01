<template>
  <v-card :color="module.is_highlighted ? '#FFF9BF' : 'white'" height="100%">
    <v-card-title>
      <v-select
        v-if="available.length > 1"
        v-model="activeMod"
        :items="available"
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
      :module="module.name"
    />
  </v-card>
</template>

<script>
import { mapActions } from 'vuex'
export default {
  props: ['module'],

  data() {
    return {
      available: this.module.models.map((i) => i.pretty_name),
    }
  },
  computed: {
    activeMod: {
      get() {
        return this.module.pretty_name
      },
      set(val) {
        this.toFramework({
          intent: 'set_module',
          module: val,
        })
      },
    },
  },
  methods: {
    ...mapActions(['toFramework']),
  },
}
</script>

<style scoped></style>
