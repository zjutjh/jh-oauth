<template>
  <div style="display:block;">
    <span class="fieldGroup" :class="borderColor">
      <label class="ms-fontWeight-semibold root">{{label}}</label>
      <span style="border-right: solid;border-color: rgb(138, 136, 134);border-width: 1px;"></span>
      <input class="field" v-if="type=='text'" v-model="inputa" />
      <input class="field" v-if="type=='password'" type="password" v-model="vinput" />
    </span>
    <div v-if="errrText&&showerr" class="error ms-fontWeight-semibold">{{errrText}}</div>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue, Model, Emit, Watch } from 'vue-property-decorator';
type ValueCheckFunc = (source: string) => boolean;

@Component
export default class TextField extends Vue {
  @Prop() private label!: string;
  @Prop() private errrText!: string;
  @Prop() private type!: 'text' | 'password';
  @Prop() private valueCheck!: ValueCheckFunc | boolean;
  private borderColor = '';
  private vinput: string = '';
  private showerr: boolean = false;
  private check(val: string) {
    if (typeof this.valueCheck === 'boolean') {
      if (this.valueCheck as boolean) {
        this.borderColor = 'red';
        this.showerr = true;
      } else {
        this.borderColor = '';
        this.showerr = false;
      }
    } else if (this.valueCheck as ValueCheckFunc) {
      if (!(this.valueCheck as ValueCheckFunc)(val) && val !== '') {
        this.borderColor = 'red';
        this.showerr = true;
      } else {
        this.borderColor = '';
        this.showerr = false;
      }
    }
  }

  @Watch('inputa')
  private onInputChanged(val: string, oldVal: string) {
    this.check(val);
    this.change(val);
  }
  @Model('change', {
    type: String,
  })
  private input!: string;

  @Emit('change')
  private change(e: string) { }

}
</script>
<style scoped>
.fieldGroup {
  box-shadow: none;
  margin: 0;
  margin-top: 0.5rem;
  padding: 0;
  box-sizing: border-box;
  cursor: text;
  height: 3rem;
  display: flex;
  flex-direction: row;
  align-items: stretch;
  position: relative;
  border-width: 1px;
  border-style: solid;
  border-color: rgb(138, 136, 134);
  border-radius: 0.4rem;
  background: rgba(255, 255, 255, 0.6);
}
.field {
  font-family: "Segoe UI", "Segoe UI Web (West European)", "Segoe UI",
    -apple-system, BlinkMacSystemFont, Roboto, "Helvetica Neue", sans-serif;
  -webkit-font-smoothing: antialiased;
  font-weight: 400;
  box-shadow: none;
  margin: 0;
  padding-top: 0px;
  padding-right: 8px;
  padding-bottom: 0px;
  padding-left: 8px;
  box-sizing: border-box;
  color: rgb(50, 49, 48);
  width: 100%;
  border-style: none;
  background: none transparent;
  outline: 0px;
}
.root {
  margin-left: 0.3rem;
  margin-right: 0.3rem;
  text-align: start;
  white-space: nowrap;
  align-self: center;
}
.error {
  margin-left: 0.5rem;
  margin-right: 0.5rem;
  margin-top: 0.3rem;
  color: red;
  text-align: start;
}
.red {
  border-color: red;
}
</style>
