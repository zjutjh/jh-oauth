<template>
  <card :title="oauthLabel" class="auth-panel">
    <text-field class="margeTop" label="精弘通行证" type="text" v-model="id"></text-field>
    <text-field class="margeTop" label="密码" type="password" v-model="pass"></text-field>
    <div class="margeTopRight">
      <span style="margin:1rem;cursor:pointer" @click="TipClick">帮助 ❓</span>
      <span style="margin:1rem;cursor:pointer" @click="aboutClick">❕ 关于</span>
    </div>
    <v-button class="right-buttom" text="登录" @click="login(id,pass)" :waiting="isWaiting"></v-button>
    <dialog-com :show="isTipClicked" @close="close"></dialog-com>
    <dialog-com :show="isError" @close="close">
      <template v-slot:main>{{errmsg}}</template>
    </dialog-com>
  </card>
</template>
<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { postData, getData } from '../utils/fetch';
import { API, apiMap } from '../utils/api';
import { OAuthRequest, OAuthResponse } from '../interface/frontend/OAuth';
import { CheckPreResponse } from '../interface/backend/app/CheckPre';
import router from '../router';

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
  private errmsg: string = '';
  private isTipClicked: boolean = false;
  private id: string = '';
  private pass: string = '';
  private isWaiting: boolean = false;
  private login() {
    const request: any = {
      studentId: '',
      password: '',
    };
    this.isWaiting = true;
    postData(API(apiMap.authUser), request).then((res: OAuthResponse) => {
      this.isWaiting = false;
      if (!this.request) { return; }
      window.location.href = this.request.redirect_uri + '?' +
        this.request.response_type + res.token + '&state' + res.state;
    }).catch(() => {
      this.isWaiting = false;
    });
  }

  private created() {
    if (<object>this.$route.query == {}) { router.replace('/error'); return; }
    this.request = <object>this.$route.query as OAuthRequest;
    if (!this.request.client_id || !this.request.client_id ||
      !this.request.redirect_uri || !this.request.scope) { router.replace('/error'); return; }

    getData(API(apiMap.authApp)).then((res: CheckPreResponse) => {
      if (res.shortcut === 'ok') {
        this.oauthLabel = '精弘认证 登录到 ' + res.data.name;
      } else {
        router.replace('/error');
      }
    });
  }

  private aboutClick() {
    this.$router.push('/about');
  }
  private close() {
    this.isTipClicked = false;
    this.isError = false;
  }
  private TipClick() {
    this.isTipClicked = true;
  }
}
</script>