<template>
  <card title="精弘认证 登录" class="auth-panel">
    <text-field class="margeTop" label="精弘通行证" type="text" v-model="id"></text-field>
    <text-field class="margeTop" label="密码" type="password" v-model="pass"></text-field>
    <div class="margeTopRight">
      <span style="margin:1rem;cursor:pointer" @click="tipClick">帮助 ❓</span>
      <span style="margin:1rem;cursor:pointer" @click="aboutClick">❕ 关于</span>
    </div>
    <v-button class="right-buttom" text="登录" @click="login(id,pass)" :waiting="isWaiting"></v-button>
    <dialog-com :show="isTipClicked" @close="closeDialog">
      <template v-slot:main>{{errorMsg}}</template>
    </dialog-com>
    <dialog-com :show="isError" @close="closeDialog">
      <template v-slot:main>{{errorMsg}}</template>
    </dialog-com>
  </card>
</template>
<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { LoginRequest, LoginResponse } from '../interface/backend/user/Login';
import { postData, getData } from '../utils/fetch';
import router from '../router';
import { API, apiMap } from '../utils/api';
import TextField from '../components/TextField.vue';
import VButton from '../components/Button.vue';
import Card from '../components/Card.vue';
import DialogCom from '../components/Dialog.vue';
import { routerPath } from '../utils/routerPath';

@Component({
  components: { TextField, VButton, Card, DialogCom },
})
export default class Auth extends Vue {
  private isError: boolean = false;
  private errorMsg: string = '';
  private isTipClicked: boolean = false;
  private id: string = '';
  private pass: string = '';
  private isWaiting: boolean = false;
  private login(id: string, pass: string) {
    const request: LoginRequest = {
      name: id,
      password: pass,
      device_type: 'web',
    };
    this.isWaiting = true;
    postData(API(apiMap.authUser), request).then((res: LoginResponse) => {
      if (res.shortcut === 'ok') {
        router.push('/user');
      } else if (res.shortcut === 'pe') {
        this.isError = true;
        this.errorMsg = '密码错误';
      } else if (res.shortcut === 'une') {
        this.isError = true;
        this.errorMsg = '用户不存在';
      }
      this.isWaiting = false;
    }).catch(() => {
      this.isError = true;
      this.errorMsg = '服务器问题';
      this.isWaiting = false;
    });
  }

  private aboutClick() {
    this.$router.push(routerPath.about);
  }
  private closeDialog() {
    this.isTipClicked = false;
    this.isError = false;
  }
  private tipClick() {
    this.isTipClicked = true;
  }
}
</script>