<template>
  <div>
    <v-card width="100%" height="500px" class="mb-12 mt-3">
      <div class="chat-container">
        <v-row
          v-for="(item, index) in tuningChat"
          :key="index"
          class="pa-2"
          :class="{ 'flex-row-reverse': !item.isBot }"
        >
          <v-col :cols="3"> A </v-col>
          <v-col :cols="8">
            <v-card :color="item.isBot ? 'blue' : 'red'">
              <div class="text--primary">
                {{ item.message }}
              </div>
            </v-card>
          </v-col>
        </v-row>
      </div>

      <v-row align="center" class="align-self-end chat-interface">
        <v-col :cols="7">
          <v-text-field
            v-model="utterance"
            background-color="grey lighten-3"
          ></v-text-field>
        </v-col>
        <v-col :cols="2"
          ><v-btn color="primary" @click="toFramework(utterance)">
            Send
          </v-btn></v-col
        >
      </v-row>
    </v-card>
  </div>
</template>

<script>
import { mapActions, mapState } from 'vuex'
export default {
  components: {},
  data() {
    return {
      utterance: '',
    }
  },
  computed: {
    ...mapState(['tuningChat']),
  },
  methods: {
    ...mapActions(['toFramework']),
  },
}
</script>

<style scoped>
.chat-interface {
  position: absolute;
  bottom: 0;
}

.chat-container {
  height: 450px;
  overflow-y: auto;
  overflow-x: hidden;
}
</style>
