<template>
  <div>
    <v-card class="mb-12" height="25px">
      MODULE: {{ module.pretty_name }}
    </v-card>
  </div>
</template>

<script>
export default {
  props: ['module'],
}
</script>

<style scoped></style>
