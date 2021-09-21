<template>
  <div>
    <div class="chat-container">
      <v-row
        v-for="(item, index) in tuningChat"
        :key="index"
        :class="{ 'flex-row-reverse': !item.isBot }"
      >
        <v-col :cols="3">
          <!--  TODO: make icon -->
          A
        </v-col>
        <v-col :cols="8">
          <v-card :color="item.isBot ? 'white' : 'accent'">
            <div class="text--primary">
              {{ item.message }}
            </div>
          </v-card>
        </v-col>
      </v-row>
    </div>

    <div>
      <v-row align="center">
        <v-col :cols="9">
          <v-text-field
            v-model="utterance"
            height="35"
            :rounded="true"
            background-color="grey lighten-3"
          />
        </v-col>
        <v-col :cols="1">
          <v-btn
            color="primary"
            :rounded="true"
            :depressed="true"
            @click="sendText"
          >
            <!--  TODO: make icon -->
            ➤
          </v-btn>
        </v-col>
      </v-row>
    </div>
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
    sendText() {
      this.toFramework(this.utterance)
      this.utterance = ''
    },
  },
}
</script>

<style scoped>
.chat-container {
  height: 450px; /* This component is 450px tall. Deal with it. */
  overflow-y: auto; /*TODO: keep scroll to bottom */
  overflow-x: hidden;
}
</style>
