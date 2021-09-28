<template>
  <div>
    <v-container fluid>
      <v-row>
        <v-col id="chat" flat class="chat-container">
          <v-row
            v-for="(item, index) in tuningChat"
            :key="index"
            :class="{ 'flex-row-reverse': !item.isBot }"
          >
            <v-col :cols="2">
              <font-awesome-icon
                :icon="item.isBot ? 'lightbulb' : 'user'"
                size="2x"
                color="#424242"
              />
            </v-col>
            <v-col :cols="9">
              <v-card
                :color="item.isBot ? 'white' : 'accent'"
                class="py-1 px-2"
              >
                {{ item.message }}
              </v-card>
            </v-col>
          </v-row>
        </v-col>
      </v-row>

      <v-row dense>
        <v-col xl="10" lg="9" md="8" sm="7">
          <v-textarea
            v-model="utterance"
            solo
            flat
            no-resize
            label="Write here to chat"
            rows="3"
            background-color="grey lighten-3"
            hide-details="true"
            @keyup.enter="sendText"
          ></v-textarea>
        </v-col>

        <v-col cols="2" class="align-self-stretch">
          <v-btn
            height="100%"
            color="primary"
            :depressed="true"
            @click="sendText"
          >
            <font-awesome-icon icon="chevron-right" size="2x" color="white" />
          </v-btn>
        </v-col>
      </v-row>
    </v-container>
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
  updated() {
    this.scrollToEnd()
  },
  methods: {
    ...mapActions(['toFramework']),
    sendText() {
      if (this.utterance.trim() !== '' && this.utterance !== '\n') {
        this.toFramework(this.utterance)
        this.utterance = ''
      }
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
  height: 600px; /* This component is 450px tall. Deal with it. */
  overflow-y: auto;
  overflow-x: hidden;
}
</style>
