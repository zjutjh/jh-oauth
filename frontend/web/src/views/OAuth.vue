 <template>
  <card :title="oauthLabel" class="auth-panel">
    <div v-if="!isAutoLogin">
      <text-field
        class="margeTop"
        label="精弘通行证"
        type="text"
        v-model="id"
        :valueCheck="idFilter"
        errrText="请输入正确的精弘通行证"
      ></text-field>
      <text-field class="margeTop" label="密码" type="password" v-model="pass"></text-field>
      <v-button style="margin:1rem" text="登录" @click="login" :waiting="isWaiting"></v-button>
    </div>
    <div v-else>
      <text-field
        class="margeTop"
        label="精弘通行证"
        type="text"
        v-model="id"
        :valueCheck="idFilter"
        errrText="请输入正确的精弘通行证"
        disable="true"
      ></text-field>
      <v-button style="margin:1rem" text="自动登录" @click="autoLogin" :waiting="isWaiting"></v-button>
      <v-button style="margin:1rem" text="清除记录" @click="autoLogout" :waiting="isWaiting"></v-button>
    </div>
    <div class="margeTopRight">
      <span style="margin:1rem;cursor:pointer" @click="tipClick">帮助 ❓</span>
      <span style="margin:1rem;cursor:pointer" @click="aboutClick">❕ 关于</span>
    </div>
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
import { CheckPreRequest, CheckPreResponse } from '../interface/backend/app/CheckPre';
import { LoginRequest, LoginResponse } from '../interface/backend/user/Login';
import { AutoLoginRequest, AutoLoginResponse } from '../interface/backend/user/AutoLogin';
import { OAuthLoginRequest, OAuthLoginResponse } from '../interface/backend/oauth/Auth';

import { Error } from '../utils/error';

import { routerPath } from '../utils/routerPath';
import TextField from '../components/TextField.vue';
import VButton from '../components/Button.vue';
import Card from '../components/Card.vue';
import DialogCom from '../components/Dialog.vue';

import BaseView from '../views/BaseView.vue';
import { LogoutRequest, LogoutResponse } from '../interface/backend/user/Logout';
@Component({ components: { TextField, VButton, Card, DialogCom } })
export default class OAuth extends BaseView {
  private request: OAuthRequest | undefined;
  private oauthLabel = '';
  private id: string = '';
  private pass: string = '';
  private isAutoLogin = false;
  private login() {
    if (!this.request) { this.setError(Error.requestError); return; }
    if (!this.checkInput()) { this.setError(Error.InputError); return; }

    const loginRequest: LoginRequest = {
      name: this.id,
      password: this.pass,
      device_type: 'pc',
    };

    this.isWaiting = true;
    postData(API(apiMap.authUser), loginRequest)
      .then((res: LoginResponse) => {
        if (res.shortcut !== 'ok') { throw res.msg; }
        localStorage.setItem('token', res.data.token);
        this.getAuthInfo(res.data.token).then((code) => { this.redirect(code.data); });
      })
      .catch((e) => { this.setError(e); });
  }

  private autoLogin() {
    const tk = localStorage.getItem('token');
    if (tk === null) { this.isAutoLogin = false; return; }
    this.getAuthInfo(tk).then((code) => { this.redirect(code.data); });
  }
  private autoLogout() {
    this.isAutoLogin = false;
    const tk = localStorage.getItem('token');
    localStorage.removeItem('token');
    if (tk === null) { this.isAutoLogin = false; return; }
    const logoutRequest: LogoutRequest = {
      token: tk,
    };

    this.isWaiting = true;
    postData(API(apiMap.logout), logoutRequest)
      .then((res: LogoutResponse) => {
        if (res.shortcut !== 'ok') { throw res.msg; }
        this.$router.push(routerPath.success);
      })
      .catch((e) => { this.setError(e); });
  }

  private getAuthInfo(tk: string): Promise<OAuthLoginResponse> {
    if (!this.request) { throw Error.requestError; }

    const OARequest: OAuthLoginRequest = {
      token: tk,
      appname: this.request.client_id,
      title: '我也不知道这是啥',
    };
    this.isWaiting = true;
    return postData(API(apiMap.oauth), OARequest)
      .then((res: OAuthLoginResponse) => {
        this.isWaiting = false;
        if (!this.request || res.shortcut !== 'ok') { throw Error.unknow; }
        return res;
      });
  }

  private getAutoLoginInfo() {
    const tk = localStorage.getItem('token');
    if (tk === null) { this.isAutoLogin = false; return; }
    const loginRequest: AutoLoginRequest = {
      token: tk,
    };

    this.isWaiting = true;
    postData(API(apiMap.autoUser), loginRequest)
      .then((res: AutoLoginResponse) => {
        if (res.shortcut !== 'ok') { throw res.msg; }
        localStorage.setItem('token', res.data.token);
        this.id = res.data.username;
      })
      .catch((e) => { this.setError(e); });
  }
  private getAppInfo() {

    if (!this.request) { this.setError(Error.requestError); return; }
    const OARequest: CheckPreRequest = {
      appname: this.request.client_id,
    };
    this.isWaiting = true;
    getData(API(apiMap.authApp))
      .then((res: CheckPreResponse) => {
        this.isWaiting = false;
        if (res.shortcut !== 'ok') { this.$router.replace(routerPath.invalid); return; }
        this.oauthLabel = '精弘认证 登录到 ' + res.data.name;
      })
      .catch(() => { this.setError(Error.unknow); });
  }
  private redirect(code: string) {
    if (!this.request || code === '') { throw Error.unknow; }
    window.location.href = this.request.redirect_uri + '?' +
      this.request.response_type + code + '&state' + this.request.state;
  }
  private checkInput() {
    return this.id !== '' && this.pass !== '' && this.idFilter(this.id);
  }

  private getQuery() {
    this.request = this.$route.query as unknown as OAuthRequest;
    if (!this.request || !this.request.client_id || !this.request.redirect_uri || !this.request.scope) {
      this.$router.replace(routerPath.invalid);
      return false;
    }
  }

  private created() {
    if (!this.getQuery()) { return; }
    this.getAppInfo();
    this.getAutoLoginInfo();
  }
}
</script>
