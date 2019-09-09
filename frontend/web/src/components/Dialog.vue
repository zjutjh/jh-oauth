 <template>
  <div class="dialog dialog-cover back" v-if="show">
    <!-- transition 这里可以加一些简单的动画效果 -->
    <transition name="drop">
      <div class="middle">
        <!--style 通过props 控制内容的样式  -->
        <div class="dialog-content card ms-depth-64" style="padding:0.5rem;">
          <div class="dialog_head back ms-fontWeight-bold">
            <!--弹窗头部 title-->
            <slot name="header">提示信息</slot>
          </div>
          <div class="dialog_main">
            <!--弹窗的内容-->
            <slot
              name="main"
            >Lorem ipsum dolor, sit amet consectetur adipisicing elit. Et sunt atque repellat sint laboriosam libero possimus doloremque, itaque ipsa voluptatum molestias, corporis explicabo aliquid quasi accusantium illo a quo quam?</slot>
          </div>
          <!--弹窗关闭按钮-->
          <v-button @click="closed" class="margeBottom">关闭</v-button>
        </div>
      </div>
    </transition>
  </div>
</template> 

<style scoped>
.dialog_main {
  margin-top: 1rem;
  margin-bottom: 2rem;
}
.margeBottom {
  position:static;
  left: 40%;
  right: 40%;
  text-align: center;
}
/* 最外层 设置position定位 */
.dialog {
  position: relative;
  color: #2e2c2d;
  display: table;
  vertical-align: middle;
}
/*  遮罩 设置背景层，z-index值要足够大确保能覆盖，高度 宽度设置满 做到全屏遮罩 */
.dialog-cover {
  position: fixed;
  z-index: 200;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}
/* 内容层 z-index要比遮罩大，否则会被遮盖， */
.dialog-content {
  max-width: 20rem;
  border-radius: 2rem;
  margin-right: auto;
  margin-left: auto;
  z-index: 300;
  backdrop-filter: blur(1rem);
  background: white;
  min-height: 10rem;
}
</style>
<script lang="ts">
import { Component, Prop, Vue, Emit } from 'vue-property-decorator';
import VButton from '@/components/Button.vue';
@Component({
  components: { VButton },
})
export default class Dialog extends Vue {
  @Prop() private show!: boolean;
  @Emit()
  private close() { }
  private closed() {
    this.close();
  }
}
</script>
