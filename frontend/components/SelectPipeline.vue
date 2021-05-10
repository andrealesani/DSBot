<template>
  <div>
    <v-card class="mb-12" height="200px">
      <v-radio-group v-model="selectedOperation">
        <v-radio
          v-for="operation in operationsArray"
          :key="operation.operation_id"
          :label="operation.request"
          :value="operation.operation_id"
        ></v-radio>
      </v-radio-group>
    </v-card>
    <!-- <v-btn color="primary"> Continue </v-btn> -->
    <!-- <v-btn color="primary" @click="e1 = 2"> Continue </v-btn> -->
  </div>
</template>

<script>
import { mapState, mapMutations } from 'vuex'

export default {
  components: {},
  data() {
    return {
      selectedOperation: -1,
    }
  },
  methods: {
    ...mapMutations(['setStep']),
  },
  computed: {
    ...mapState(['operationsArray']),
  },
}
</script>
