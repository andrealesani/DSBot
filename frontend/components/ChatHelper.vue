<template>
  <v-col>
    <v-row justify="center">
      <v-col>
        <!--      <v-img :src="require('@/assets/clusters_img.png')" aspect-ratio="1.8" />-->
        <transition name="bounce">
          <img
            v-if="imageBase64 !== null"
            :src="`data:image/png;base64,${imageBase64}`"
            alt=""
          />
          <div v-else class="GUIHelper">
            <p>
              <font-awesome-icon icon="question" size="2x" color="#115e63ff" />
            </p>
            <br />
            <p>This section is dedicated to helping you with your choices</p>
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
    ...mapState(['imageBase64', 'resultsDetails']),
  },
}
</script>
<style scoped>
img {
  max-width: 100%;
  max-height: 100%;
  height: auto;
}

.GUIHelper {
  background: #d4d4d4;
  min-height: 400px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 10px;
  font-family: 'Open Sans', Verdana, sans-serif;
  color: #115e63ff;
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
