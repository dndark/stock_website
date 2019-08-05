import Vue from 'vue'
import Router from 'vue-router'
// import New from '@/components/New'
// import In from "@/components/In"
// import Overview from "@/components/Overview"
// import Out from "@/components/Out"
// import Pending from "@/components/Pending"
// import ReIn from "@/components/ReIn"
// import StockOverDue from "@/components/StockOverDue"
// import UnPay from "@/components/UnPay"
// import UnPayDetail from "@/components/UnPayDetail"
// import InProgress from "@/components/InProgress"

// import Handled from "@/components/Handled"
Vue.use(Router)

export default new Router({
  routes: [
    // {
    //   path: '/new',
    //   name: 'New',
    //   component: New
    // },
    // {
    //   path: '/in',
    //   name: 'In',
    //   component: In
    // },
    // {
    //   path: '/out',
    //   name: 'Out',
    //   component: Out
    // },
    // {
    //   path: '/pending',
    //   name: 'Pending',
    //   component: Pending
    // },
    // {
    //   path: '/reIn',
    //   name: 'ReIn',
    //   component: ReIn
    // },
    // {
    //   path: '/',
    //   name: 'Overview',
    //   component: Overview
    // },
    // {
    //   path: '/',
    //   name: 'StockOverDue',
    //   component: StockOverDue
    // },
    // {
    //   path: '/unPay',
    //   name: 'UnPay',
    //   component: UnPay
    // },
    // {
    //   path: '/unPayDetail',
    //   name: 'UnPayDetail',
    //   component: UnPayDetail
    // },
    // {
    //   path: '/inProgress',
    //   name: 'InProgress',
    //   component: InProgress
    // },
    // {
    //   path: '/handled',
    //   name: 'Handled',
    //   component: Handled
    // },
  {
    path: '/',
    name: 'StockOverDue',
    component: resolve => require(["@/components/StockOverDue"],resolve)
  },
  {
    path: '/unPay',
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
  ],
  mode: 'history',
})


