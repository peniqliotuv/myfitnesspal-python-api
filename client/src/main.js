import 'babel-polyfill';
import Vue from 'vue'
import App from './App.vue'
import router from './router/index';

const app = new Vue({
  el: '#app',
  router,
  render: h => h(App)
});
