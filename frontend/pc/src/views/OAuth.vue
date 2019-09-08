 <template>
  <card :title="oauthLabel" class="auth-panel">
    <text-field
      class="margeTop"
      label="精弘通行证"
      type="text"
      v-model="id"
      :valueCheck="idFilter"
      errrText="请输入正确的精弘通行证"
    ></text-field>
    <text-field class="margeTop" label="密码" type="password" v-model="pass"></text-field>
    <div class="margeTopRight">
      <span style="margin:1rem;cursor:pointer" @click="tipClick">帮助 ❓</span>
      <span style="margin:1rem;cursor:pointer" @click="aboutClick">❕ 关于</span>
    </div>
    <v-button text="登录" @click="login(id,pass)" :waiting="isWaiting"></v-button>
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
import { LoginRequest, LoginResponse } from '../interface/backend/user/Login';
import { OAuthLoginRequest, OAuthLoginResponse } from '../interface/backend/oauth/Auth';

import { Error } from '../utils/error';

import { routerPath } from '../utils/routerPath';
import TextField from '../components/TextField.vue';
import VButton from '../components/Button.vue';
import Card from '../components/Card.vue';
import DialogCom from '../components/Dialog.vue';

import BaseView from '../views/BaseView.vue';
@Component({ components: { TextField, VButton, Card, DialogCom } })
export default class OAuth extends BaseView {
  private request: OAuthRequest | undefined;
  private oauthLabel = '';
  private id: string = '';
  private pass: string = '';

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
        this.getAuthCode(res, loginRequest);
      })
      .catch((e) => { this.setError(e); });
  }

  private getAuthCode(loginResponse: LoginResponse, loginRequest: LoginRequest) {
    if (!this.request) { throw Error.requestError; }

    const OARequest: OAuthLoginRequest = {
      token: loginResponse.data.token,
      appname: this.request.client_id,
      title: '我也不知道这是啥',
    };

    postData(API(apiMap.oauth), loginRequest)
      .then((res: OAuthLoginResponse) => {
        this.isWaiting = false;
        if (!this.request || res.shortcut !== 'ok') { throw Error.unknow; }
        window.location.href = this.request.redirect_uri + '?' +
          this.request.response_type + res.data + '&state' + this.request.state;
      });
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
  }

  private getAppInfo() {
    this.isWaiting = true;
    getData(API(apiMap.authApp))
      .then((res: CheckPreResponse) => {
        this.isWaiting = false;
        if (res.shortcut !== 'ok') { this.$router.replace(routerPath.invalid); return; }
        this.oauthLabel = '精弘认证 登录到 ' + res.data.name;
      })
      .catch(() => { this.setError(Error.unknow); });
  }
}
</script>
