import Vue from 'vue';
import Router from 'vue-router';
import Home from './views/Home.vue';

Vue.use(Router);

export default new Router({
  mode: 'hash',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/dev',
      name: 'dev',
      component: () => import(/* webpackChunkName: "devcenter" */ './views/DevCenter.vue'),
      meta: {
        title: '开发者中心',
      },
    },
    {
      path: '/user',
      name: 'user',
      component: () => import(/* webpackChunkName: "usercenter" */ './views/User.vue'),
      meta: {
        title: '用户中心',
      },
    },
    {
      path: '/',
      component: Home,
      children: [
        {
          path: '/',
          name: 'auth',
          component: () => import(/* webpackChunkName: "auth" */ './views/Auth.vue'),
          meta: {
            title: '用户中心认证',
          },
        },
        {
          path: '/oauth',
          name: 'oauth',
          component: () => import(/* webpackChunkName: "auth" */ './views/OAuth.vue'),
          meta: {
            title: '用户开放认证',
          },
        },
        {
          path: '/about',
          name: 'about',
          component: () => import(/* webpackChunkName: "auth" */ './views/About.vue'),
          meta: {
            title: '关于',
          },
        },
        {
          path: '/act',
          name: 'act',
          component: () => import(/* webpackChunkName: "auth" */ './views/Activation.vue'),
          meta: {
            title: '用户激活',
          },
        },
        {
          path: '/reset',
          name: 'reset',
          component: () => import(/* webpackChunkName: "auth" */ './views/Reset.vue'),
          meta: {
            title: '重设密码',
          },
        },
        {
          path: '/success',
          name: 'success',
          component: () => import(/* webpackChunkName: "auth" */ './views/Success.vue'),
          meta: {
            title: '成功',
          },
        },
        {
          path: '/invalid',
          name: 'invalid',
          component: () => import(/* webpackChunkName: "auth" */ './views/Invalid.vue'),
          meta: {
            title: 'invalid',
          },
        },
        {
          // 会匹配所有路径
          path: '*',
          component: () => import(/* webpackChunkName: "auth" */ './views/NotFind.vue'),
          meta: {
            title: '404',
          },
        },
      ],
    },
  ],
});
