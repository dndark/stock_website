import Vue from 'vue'
import Router from 'vue-router'
import New from '@/components/New'
import In from "@/components/in"
import Overview from "@/components/Overview"
import Out from "@/components/Out"
import Pending from "@/components/Pending"

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/new',
      name: 'New',
      component: New
    },
    {
      path: '/',
      name: 'Overview',
      component: Overview
    },
    {
      path: '/in',
      name: 'In',
      component: In
    },
    {
      path: '/out',
      name: 'Out',
      component: Out
    },
    {
      path: '/pending',
      name: 'Pending',
      component: Pending
    },
    
  ],
  mode: 'history',
})


