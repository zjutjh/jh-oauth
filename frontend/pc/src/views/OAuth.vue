<template>
  <card :title="oauthLabel" class="auth-panel">
    <text-field class="margeTop" label="精弘通行证" type="text" v-model="id"></text-field>
    <text-field class="margeTop" label="密码" type="password" v-model="pass"></text-field>
    <div class="margeTopRight">
      <span style="margin:1rem;cursor:pointer" @click="tipClick">帮助 ❓</span>
      <span style="margin:1rem;cursor:pointer" @click="aboutClick">❕ 关于</span>
    </div>
    <v-button class="right-buttom" text="登录" @click="login(id,pass)" :waiting="isWaiting"></v-button>
    <dialog-com :show="isTipClicked" @close="closeDialog">
      <template v-slot:main>{{tipMsg}}</template>
    </dialog-com>
    <dialog-com :show="isError" @close="closeDialog">
      <template v-slot:main>{{errorMsg}}</template>
    </dialog-com>
  </card>
</template>
<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { postData, getData } from '../utils/fetch';
import { API, apiMap } from '../utils/api';
import { OAuthRequest, OAuthCodeResponse, OAuthError } from '../interface/frontend/OAuth';
import { CheckPreResponse } from '../interface/backend/app/CheckPre';

import { routerPath } from '../utils/routerPath';
import TextField from '../components/TextField.vue';
import VButton from '../components/Button.vue';
import Card from '../components/Card.vue';
import DialogCom from '../components/Dialog.vue';

@Component({
  components: { TextField, VButton, Card, DialogCom },
})
export default class OAuth extends Vue {
  private request: OAuthRequest | undefined;
  private oauthLabel = '';
  private isError: boolean = false;
  private errorMsg: string = '';
  private isTipClicked: boolean = false;
  private tipMsg: string = '';
  private id: string = '';
  private pass: string = '';
  private isWaiting: boolean = false;
  private login() {
    const request: any = {
      studentId: '',
      password: '',
    };
    this.isWaiting = true;
    postData(API(apiMap.authUser), request).then((res: OAuthCodeResponse) => {
      this.isWaiting = false;
      if (!this.request) { return; }
      window.location.href = this.request.redirect_uri + '?' +
        this.request.response_type + res.code + '&state' + res.state;
    }).catch(() => {
      this.isWaiting = false;
      this.isError = true;
    });
  }

  private created() {
    if (<object>this.$route.query === {}) { this.$router.replace(routerPath.invalid); return; }
    this.request = <object>this.$route.query as OAuthRequest;
    if (!this.request.client_id || !this.request.client_id ||
      !this.request.redirect_uri || !this.request.scope) { this.$router.replace(routerPath.invalid); return; }

    getData(API(apiMap.authApp)).then((res: CheckPreResponse) => {
      if (res.shortcut === 'ok') {
        this.oauthLabel = '精弘认证 登录到 ' + res.data.name;
      } else {
        this.$router.replace(routerPath.invalid);
      }
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
