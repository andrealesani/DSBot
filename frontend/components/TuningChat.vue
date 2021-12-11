<template>
  <div>
    <!-- Chat history container -->
    <v-container fluid>
      <v-row>
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
                  color="#424242"
                />
              </v-col>
              <v-col
                :cols="7"
                :class="
                  item.isBot ? 'd-flex justify-start' : 'd-flex justify-end'
                "
              >
                <v-card
                  dark
                  :color="item.isBot ? '#115e63' : '#182859'"
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
        </v-col>
      </v-row>

      <!-- Area where u write the message -->
      <v-row dense>
        <v-col xl="10" lg="9" md="8" sm="7">
          <v-textarea
            v-model="utterance"
            solo
            flat
            no-resize
            label="Write here to chat"
            rows="3"
            background-color="#d4d4d4"
            hide-details="true"
            @keyup.enter="sendText"
          ></v-textarea>
        </v-col>

        <!-- 'Send message' button -->
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
    ...mapState(['tuningChat']),
  },
  updated() {
    this.scrollToEnd()
  },
  methods: {
    ...mapActions(['toFramework', 'sendChatMessage']),
    sendText() {
      // check that the user has effectively written something
      if (this.utterance.trim() !== '' && this.utterance !== '\n') {
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
  height: 600px; /* This component is this tall. Deal with it. */
  overflow-y: auto;
  overflow-x: hidden;
}

.message-bubble {
  padding: 5pt 12pt;
  block-size: fit-content;
  inline-size: fit-content;
  border-radius: 30px !important;
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
