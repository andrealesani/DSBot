<template>
  <v-card flat>
    <v-card id="chat" flat class="chat-container">
      <v-row
        v-for="(item, index) in tuningChat"
        :key="index"
        :class="{ 'flex-row-reverse': !item.isBot }"
      >
        <v-col :cols="3">
          <!--  TODO: make icon -->
          <font-awesome-icon icon="user" />
        </v-col>
        <v-col :cols="8">
          <v-card :color="item.isBot ? 'white' : 'accent'">
            <div class="text--primary">
              {{ item.message }}
            </div>
          </v-card>
        </v-col>
      </v-row>
    </v-card>

    <v-card flat>
      <v-row dense align="center">
        <v-col cols="8" sm="8" md="8">
          <!-- <v-text-field
            v-model="utterance"
            height="35"
            :rounded="true"
            background-color="grey lighten-3"
            @keyup.enter="sendText"
          /> -->
          <v-textarea
            v-model="utterance"
            solo
            flat
            no-resize
            name="input-7-4"
            label="Solo textarea"
            rows="3"
            :rounded="false"
            background-color="grey lighten-3"
            @keyup.enter="sendText"
          ></v-textarea>
        </v-col>
        <v-col cols="1" sm="1" md="1">
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
    </v-card>
  </v-card>
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
  updated() {
    this.scrollToEnd()
  },
  methods: {
    ...mapActions(['toFramework']),
    sendText() {
      this.toFramework(this.utterance)
      this.utterance = ''
    },
    scrollToEnd() {
      const container = this.$el.querySelector('#chat')
      // console.log(container);
      if (container) {
        container.scrollTop = container.scrollHeight
      }
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
