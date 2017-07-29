import Vue from 'vue'
import VueRouter from 'vue-router';
import Login from '../components/Login.vue';
import HomePage from '../components/HomePage.vue';

Vue.use(VueRouter);

const routes = [
  { 
    path: '/', 
    name: 'Login',
    component: Login,
  },
  {
    path: '/home/:id',
    name: 'HomePage',
    component: HomePage,
  }
];

const router = new VueRouter({ routes });

export default router;