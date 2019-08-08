<template>
<div>
  <b-navbar toggleable="lg" type="dark" variant="primary" >
    <b-navbar-brand disabled>库房系统</b-navbar-brand>

    <!-- <b-navbar-toggle target="nav_collapse" /> -->

    <b-collapse is-nav id="nav_collapse">
      <b-navbar-nav v-show="isLogined()">
        <b-nav-item-dropdown  text="货款跟进" left>
           <b-dropdown-item href="/" >未付款</b-dropdown-item>
          <b-dropdown-item href="inProgress" >处理中</b-dropdown-item>
          <b-dropdown-item href="handled" >已处理</b-dropdown-item>
          <b-dropdown-item href="paid" >已付款</b-dropdown-item>
        </b-nav-item-dropdown>

        <b-nav-item-dropdown text="库房跟进" left>
           <b-dropdown-item  href="stockOverDue" >3月未提货</b-dropdown-item>
        </b-nav-item-dropdown>
        <b-nav-item href="unPayDetail" v-show="isLogined()">合同查询</b-nav-item>
      </b-navbar-nav>

      <b-navbar-nav class="ml-auto">
        <div v-show="isLogined()">
        <b-nav-item class='ml-auto' disabled v-if='this.isAdmin()'>管理员:{{this.userInfo}}</b-nav-item>
        <b-nav-item class='ml-auto' disabled v-else> 业务员:{{this.userInfo}}</b-nav-item>
        </div>
        <b-nav-item class="ml-auto" v-show="isLogined()" @click="logout()">退出登录</b-nav-item>
      </b-navbar-nav>

    </b-collapse>
  </b-navbar>
</div>
   
</template>

<script>

import Login from '@/components/Login'
export default {
    computed: {
      userInfo(){
        return this.$store.state.userInfo ||this.getCookie('userInfo')
      }
    },
    methods: {
      isLogined(){
        return this.$store.state.logined
      },
      logout(){
        this.delCookie('session');
        this.delCookie('userInfo')
        this.delCookie('permission')
        this.$router.push('/login/');
        
        this.$store.commit('logout')
      },
      isAdmin(){
        return this.getCookie("permission")==="admin"
      }
    },
    created(){
      this.isAdmin()
    },
    name:"Navbar",
    // mixins: [Login]
}
</script>

