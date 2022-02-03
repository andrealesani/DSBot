<template>
  <div>
    <!-- Chat history container -->
    <v-container fluid>
      <v-col id="chat" flat class="chat-container">
        <!-- For evey message print the icon and the v-card -->
        <transition-group name="bounce">
          <v-row
            v-for="(item, index) in tuningChat"
            :key="index"
            :class="{ 'flex-row-reverse': !item.isBot }"
          >
            <v-col :cols="1">
              <font-awesome-icon
                :icon="item.isBot ? 'robot' : 'user'"
                size="2x"
                color="#555555"
              />
            </v-col>
            <v-col
              :cols="8"
              :class="
                item.isBot ? 'd-flex justify-start' : 'd-flex justify-end'
              "
            >
              <v-card
                dark
                :color="item.isBot ? 'bot' : 'user'"
                class="message-bubble"
              >
                {{
                  !item.isBot || item.message !== '#wait' ? item.message : ''
                }}
                <div v-if="item.isBot && item.message === '#wait'">
                  <div class="typing__dot"></div>
                  <div class="typing__dot"></div>
                  <div class="typing__dot"></div>
                </div>
              </v-card>
            </v-col>
          </v-row>
        </transition-group>
        <v-spacer></v-spacer>
      </v-col>

      <!-- Area where u write the message -->
      <v-row dense>
        <v-col xl="9" lg="9" md="8" sm="7">
          <v-textarea
            v-model="utterance"
            solo
            flat
            no-resize
            class="my-text-area"
            :label="botIsTyping ? 'Bot is typing' : 'Write here to chat'"
            rows="2"
            :background-color="botIsTyping ? '#dcdcdc' : '#bbdbdb'"
            hide-details="true"
            :disabled="botIsTyping"
            @keyup.enter="sendText"
          ></v-textarea>
        </v-col>

        <!-- 'Send message' button -->
        <v-col cols="1" class="align-self-stretch">
          <v-btn
            height="100%"
            color="secondary"
            :depressed="true"
            @click="sendText"
          >
            <font-awesome-icon icon="chevron-right" size="2x" color="white" />
          </v-btn>
        </v-col>

        <!-- 'HELP' button -->
        <v-col cols="1">
          <v-btn
            height="100%"
            :color="showHelp ? 'secondary' : '#3a497d'"
            :depressed="true"
            @click="userHelp"
          >
            <font-awesome-icon icon="question" size="2x" color="white" />
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
  props: {
    destination: {
      type: String,
      default: 'mmcc',
    },
  },
  data() {
    return {
      utterance: '',
    }
  },
  computed: {
    ...mapState(['tuningChat', 'botIsTyping', 'showHelp']),
  },
  updated() {
    this.scrollToEnd()
  },
  methods: {
    ...mapActions(['toFramework', 'sendChatMessage', 'getHelp']),
    userHelp() {
      this.getHelp()
    },
    sendText() {
      // check that the user has effectively written something
      if (
        this.utterance.trim() !== '' &&
        this.utterance !== '\n' &&
        !this.botIsTyping // this should never be false because textarea is disabled turing typing
      ) {
        // if the chat component is being used to communicate with mmcc
        if (this.destination === 'mmcc') this.toFramework(this.utterance)
        else
          this.sendChatMessage({
            destination: this.destination,
            payload: this.utterance,
          })
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
  min-height: 500px;
  max-height: 700px;
  min-width: 500px;
  height: fit-content;
  overflow-y: auto;
  overflow-x: hidden;
  display: flex;
  flex-direction: column-reverse;
}

.message-bubble {
  padding: 5pt 12pt;
  block-size: fit-content;
  inline-size: fit-content;
  border-radius: 30px !important;
  font-size: medium;
  font-family: 'Open Sans', Verdana, sans-serif;
}

/* ANIMATIONS AND TRANSITIONS */

.bounce-enter-active {
  animation: bounce-in 0.3s;
}
.bounce-leave-active {
  animation: bounce-in 0.5s reverse;
}
@keyframes bounce-in {
  0% {
    transform: scale(0);
  }
  50% {
    transform: scale(1.1);
  }
  100% {
    transform: scale(1);
  }
}

/* 'BOT IS TYPING' ANIMATION */

.typing__dot {
  float: left;
  width: 8px;
  height: 8px;
  margin: 0 4px;
  background: #8cb8a8;
  border-radius: 50%;
  opacity: 0;
  animation: loadingFade 1s infinite;
}

.typing__dot:nth-child(1) {
  animation-delay: 0s;
}

.typing__dot:nth-child(2) {
  animation-delay: 0.2s;
}

.typing__dot:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes loadingFade {
  0% {
    opacity: 0;
  }
  50% {
    opacity: 0.8;
  }
  100% {
    opacity: 0;
  }
}
</style>
