<template>
<div>
  <b-navbar toggleable="lg" type="dark" variant="primary" >
    <b-navbar-brand disabled>库房系统</b-navbar-brand>

    <!-- <b-navbar-toggle target="nav_collapse" /> -->

    <b-collapse is-nav id="nav_collapse">
      <b-navbar-nav  >
        <!-- <> -->
        <!-- <b-nav-item ></b-nav-item> -->
        <b-nav-item href="/" v-show="isLogined()">未付款</b-nav-item>
        <b-nav-item href="inProgress" v-show="isLogined()">处理中</b-nav-item>
        <b-nav-item href="handled" v-show="isLogined()">已处理</b-nav-item>
        
        <b-nav-item href="/stockOverDue" v-show="isLogined()">3月未提货</b-nav-item>
      </b-navbar-nav>
      <b-navbar-nav class="ml-auto">
        <b-nav-item class="ml-auto" v-show="isLogined()" @click="logout()">退出登录</b-nav-item>
      </b-navbar-nav>
        <!-- <b-nav-item href="in">入库</b-nav-item>
        <b-nav-item href="out">出库</b-nav-item>
        <b-nav-item href="pending">待发货</b-nav-item>
        <b-nav-item href="rein">重新入库</b-nav-item> -->
      

    </b-collapse>
  </b-navbar>
</div>
   
</template>

<script>

import Login from '@/components/Login'
export default {
    methods: {
      isLogined(){
        console.log(this.$store.state.logined)
        return this.$store.state.logined
      },
      logout(){
        this.delCookie('session');
        this.$router.push('/login/');
        
        this.$store.commit('logout')
        console.log(this.$store.state.logined)
      }
    },
    name:"Navbar",
    // mixins: [Login]
}
</script>

