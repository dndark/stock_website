import Vue from 'vue'
import Router from 'vue-router'
Vue.use(Router)
export default new Router({
  routes: [
  {
    path: '/login',
    component: resolve  => require(["@/components/Login"],resolve)
  }, 
  {
    path: '/stockOverDue',
    name: 'StockOverDue',
    component: resolve => require(["@/components/StockOverDue"],resolve)
  },
  {
    path: '/',
    name: 'UnPay',
    component: resolve => require(["@/components/UnPay"],resolve)
  },
  {
    path: '/unPayDetail',
    name: 'UnPayDetail',
    component:  resolve => require(["@/components/UnPayDetail"],resolve)
  },
  {
    path: '/inProgress',
    name: 'InProgress',
    component: resolve => require(["@/components/InProgress"],resolve)
  },
  {
    path: '/handled',
    name: 'Handled',
    component: resolve => require(["@/components/Handled"],resolve)
  },
  {
    path: '/paid',
    name: 'Paid',
    component: resolve => require(["@/components/Paid"],resolve)
  },
  ],
  mode: 'history',
})

