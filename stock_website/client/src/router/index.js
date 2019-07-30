import Vue from 'vue'
import Router from 'vue-router'
import New from '@/components/New'
import In from "@/components/In"
import Overview from "@/components/Overview"
import Out from "@/components/Out"
import Pending from "@/components/Pending"
import ReIn from "@/components/ReIn"
import StockOverDue from "@/components/StockOverDue"
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
    {
      path: '/',
      name: 'StockOverDue',
      component: StockOverDue
    },
  ],
  mode: 'history',
})


