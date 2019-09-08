<template>
  <div class="home outer">
    <div class="wave-box">
      <img class="wave-1 wave" src="/img/wave.png" alt="wave" />
      <img class="wave-4 wave" src="/img/wave.png" alt="wave" />
      <img class="logo" src="/img/logoc.png" alt="the logo of jh" />
      <img class="wave-2 wave" src="/img/wave.png" alt="wave" />
      <img class="wave-3 wave" src="/img/wave.png" alt="wave" />
    </div>
    <div class="middle auth-content">
      <transition name="fade">
        <router-view />
      </transition>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
@Component
export default class Home extends Vue { }
</script>
<style scoped>
/* animation of view change */
.fade-enter-active {
  transition: opacity 0.5s;
}
.fade-leave-active {
  transition: opacity 0.5s;
  display: none;
}
.fade-enter, .fade-leave-to /* .fade-leave-active below version 2.1.8 */ {
  opacity: 0;
}

.home {
  background-image: linear-gradient(to bottom, #7acfa6, #7fcfad);
  z-index: -2;/*FireFox bug*/
}
.auth-panel {
  overflow-y: auto;
  z-index: 10;
  transition: all 1s;
  width: 30rem;
  max-height: 80%;
  min-height: 40%;
  margin-right: 10%;
  margin-left: auto;
}
.logo {
  position: absolute;
  bottom: 15rem;
  width: 10rem;
  height: 10rem;
  left: 15%;
  animation: wave-v 3s;
  animation-direction: alternate;
  animation-iteration-count: infinite;
  z-index: -1;/*FireFox bug*/
}
/* Wave */
.wave-box {
  overflow: hidden;
  width: 100%;
  position: absolute;
  bottom: 0;
  height: 100%;
}
.wave {
  transition: all 1s;
  animation: wave 10s;
  animation-direction: alternate;
  animation-iteration-count: infinite;
  position: absolute;
  opacity: 0.3;
  z-index: -1;/*FireFox bug*/
}
.wave-1 {
  bottom: 0;
}
.wave-2 {
  bottom: -3rem;
  margin-left: -10rem;
  animation-duration: 15s;
}
.wave-3 {
  bottom: -6rem;
  margin-left: -15rem;
  animation-duration: 25s;
}
.wave-4 {
  bottom: -12rem;
  margin-left: -30rem;
  animation-duration: 20s;
}
@keyframes wave {
  from {
    left: 0;
  }
  to {
    left: -100rem;
  }
}
@keyframes wave-v {
  from {
    bottom: 20rem;
  }
  to {
    bottom: 25rem;
  }
}
@media screen and (max-width: 956px) {
  .logo {
    left: calc(50% - 5rem);
    z-index: -1;/*FireFox bug*/
  }
  .auth-panel {
    z-index: 10;
    overflow-y: auto;
    transition: all 1s;
    max-height: 85%;
    min-height: 65%;
    margin-left: 0;
    margin-right: 0;
    width: unset;
    border-radius: 0;
  }
  .auth-content {
    transition: all 1s;
    vertical-align: bottom;
  }
  .wave-1 {
    top: 9%;
  }
  .wave-2 {
    top: 12%;
    margin-left: -10rem;
    animation-duration: 15s;
  }
  .wave-3 {
    top: 16%;
    margin-left: -15rem;
    animation-duration: 25s;
  }
  .wave-4 {
    bottom: 20%;
    margin-left: -30rem;
    animation-duration: 20s;
  }
  @keyframes wave-v {
    from {
      top: 5%;
    }
    to {
      top: 15%;
    }
  }
}
</style>
