<template>
  <div>
    <v-card class="mb-12" height="200px">
      <div>
        <v-progress-circular indeterminate color="green"></v-progress-circular>
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
      e1: 1,
    }
  },
}
</script>
