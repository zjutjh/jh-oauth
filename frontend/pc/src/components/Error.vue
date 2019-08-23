<template>
  <div class="card center" :class="cardDeep" @mouseout="cardUnhover" @mouseover="cardHover">
    <div class="flex-v">
      <img class="logo" src="/img/logoc.png" />
      <div class="ms-fontWeight-bold ms-fontSize-28">精弘认证 Error</div>
    </div>
    出现问题
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue, Emit } from 'vue-property-decorator';
import TextFiled from '@/components/TextFiled.vue';
import VButton from '@/components/Button.vue';
@Component({
  components: { TextFiled, VButton},
})
export default class UserAuth extends Vue {
}
</script>

<style scoped>
.logo {
  height: 2rem;
  widows: 2rem;
  margin-right: 1rem;
}
.flex-v {
  display: flex;
  flex-direction: row;
}
.right-buttom {
  position: absolute;
  bottom: 2rem;
  right: 2rem;
}
.margeTop {
  margin-top: 1rem;
  text-align: start;
}
.margeTopRight {
  margin-top: 1rem;
  text-align: end;
}
</style>
