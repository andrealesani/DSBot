<template>
  <div>
    <v-card class="mb-12" height="200px">
      <div v-if="loading" class="text-center">
        <div>
          <v-progress-circular
            indeterminate
            color="green"
            size="100"
            width="10"
          ></v-progress-circular>
        </div>

        We are performing your analysis
        <v-btn color="primary" @click="loading = false"> Continue </v-btn>
      </div>
    </v-card>
    <!-- <v-btn color="primary"> Continue </v-btn> -->
    <!-- <v-btn color="primary" @click="e1 = 2"> Continue </v-btn> -->
  </div>
</template>

<script>
export default {
  components: {},
  data() {
    return {
      loading: true,
    }
  },
}
</script>
