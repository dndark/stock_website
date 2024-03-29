// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.

import 'element-ui/lib/theme-chalk/index.css';
import ElementUI from 'element-ui';
import 'bootstrap/dist/css/bootstrap.css';
import BootstrapVue from 'bootstrap-vue';


import Vue from 'vue'

import App from './App'
import router from './router'

Vue.config.productionTip = false

Vue.use(BootstrapVue)
Vue.use(ElementUI)

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
