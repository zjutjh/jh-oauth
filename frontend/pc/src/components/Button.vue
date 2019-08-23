<template>
  <button type="button" class="root primaryColor" :class="priclass" @click="clicked">
    <div class="flexContainer">
      <div v-if="!waiting">{{text}}</div>
      <slot></slot>
      <loading v-if="waiting"></loading>
    </div>
  </button>
</template>

<script lang="ts">
import { Component, Prop, Vue, Emit, Watch } from 'vue-property-decorator';
import Loading from '../components/Loading.vue'
@Component({ components: { Loading }, })
export default class VButton extends Vue {
  private priclass: string = '';
  @Prop() private text!: string;

  @Prop() private waiting!: string;
  @Watch('waiting', { immediate: true, deep: true })
  private onWaitingChanged(val: boolean, oldVal: boolean) {
    if (val) {
      this.priclass = 'disable';
      
    } else {
      this.priclass = '';
    }

  }
  private clickTimes = 0;
  
  @Emit()
  private click() {
    this.clickTimes++;
  }
  private clicked() {
    if (this.waiting) {
      return;
    }
    this.click();
  }
}
</script>

<style scoped>
.flexContainer {
  display: flex;
  height: 100%;
  flex-wrap: nowrap;
  justify-content: center;
  align-items: center;
}
.root {
  -webkit-font-smoothing: antialiased;
  font-weight: 400;
  box-sizing: border-box;
  display: inline-block;
  text-align: center;
  cursor: pointer;
  vertical-align: top;
  padding-top: 0px;
  padding-right: 16px;
  padding-bottom: 0px;
  padding-left: 16px;
  min-width: 80px;
  height: 32px;
  user-select: none;
  outline: transparent;
  border-style: none;
  text-decoration: none;
  border-radius: 0.4rem;
  transition: background-color 0.3s;
}
.primaryColor {
  background-color: rgb(0, 120, 212);
  color: rgb(255, 255, 255);
}
.primaryColor:hover {
  background-color: rgb(0, 150, 222);
  color: rgb(255, 255, 255);
}
.disable {
  background-color: rgb(200, 200, 200);
  color: rgb(255, 255, 255);
}
</style>