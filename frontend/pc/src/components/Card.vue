<template>
  <div class="card center" :class="cardDeep" @mouseout="cardUnhover" @mouseover="cardHover">
    <div class="flex-v">
      <img class="logox" src="/img/logoc.png" />
      <div class="ms-fontWeight-bold ms-fontSize-28">{{title}}</div>
    </div>
    <slot></slot>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'vue-property-decorator';
@Component
export default class Card extends Vue {
  @Prop() private title: string|undefined;
  private cardDeep = 'ms-depth-8';
  private cardHover() {
    this.cardDeep = 'ms-depth-16';
  }
  private cardUnhover() {
    this.cardDeep = 'ms-depth-8';
  }
}
</script>

<style scoped>
.logox {
  height: 2rem;
  width: 2rem;
  margin-right: 1rem;
}
</style>
