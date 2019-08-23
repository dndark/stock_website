
<template>
  <div id="firstPage">
    <navbar></navbar>
    <br>
    <router-view/>
  </div>
</template>

<script>
import navbar from '@/components/Navbar'
import Login from '@/components/Login'

export default {
  name: 'firstPage',
  methods:{
    checkLogin(){
      //检查是否存在session
      //cookie操作方法在源码里有或者参考网上的即可
      if(!this.getCookie('session') && window.location.pathname != "/register"){
        //如果没有登录状态则跳转到登录
        this.$router.push('/login');
      }
    }
  },
  created() {
    this.checkLogin();
  },
  components: {
    navbar,
  }
}

</script>

