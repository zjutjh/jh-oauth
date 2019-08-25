import Vue from 'vue';
import App from './App.vue';
import router from './router';
import 'office-ui-fabric-core/dist/css/fabric.min.css';

Vue.config.productionTip = false;

router.beforeEach((to, from, next) => {
  /* 路由发生变化修改页面title */
  if (to.meta.title) {
    document.title = to.meta.title;
  }
  next();
});
new Vue({
  router,
  render: (h) => h(App),
}).$mount('#app');
