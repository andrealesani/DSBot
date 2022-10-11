<template>
  <v-col>
    <v-row justify="center">
      <v-col>
        <transition name="bounce">
          <div class="GUIHelper">
            <p v-if="showHelp">
              <b>
                Data Analysis Advisor is a bot that lets you approach data
                analysis even with very little knowledge about this topic
              </b>
              <br />
              <br />
              This section will be used to show you any content that might come
              useful in order to make better decisions for your analysis.
              <br />
              Be as natural as you wish during your conversation, and if you are
              stuck or need some help just ask for it in chat at any time.
              <br />
              You can also ask to restart the conversation if you mistyped
              something or you think we took the wrong path
              <br />
              <br />
              DAA will do its best to support you during each step of your
              journey!
            </p>
            <div v-else>
              <img
                v-if="imageBase64 !== null && imageBase64 !== undefined"
                :src="`data:image/png;base64,${imageBase64}`"
                alt=""
              />
              <font-awesome-icon
                v-else
                icon="robot"
                size="5x"
              ></font-awesome-icon>
            </div>
          </div>
        </transition>
      </v-col>
    </v-row>
  </v-col>
</template>

<script>
import { mapState } from 'vuex'
export default {
  computed: {
    ...mapState(['imageBase64', 'resultsDetails', 'showHelp']),
  },
  methods: {},
}
</script>
<style scoped>
img {
  max-width: 100%;
  max-height: 100%;
  height: auto;
}

.GUIHelper {
  border-style: solid;
  border-color: var(--v-primary-base);
  border-width: 0.3em;
  min-height: 400px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 10px;
  font-family: 'Open Sans', Verdana, sans-serif;
  color: var(--v-primary-base);
  padding: 3em;
  text-align: justify;
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
</style>
