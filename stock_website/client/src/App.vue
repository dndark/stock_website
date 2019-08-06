
<template>
  <div id="app">
    
    <firstPage></firstPage>
  </div>
</template>

<script>
import Vue from 'vue'
import Vuex from 'vuex'

import firstPage from './components/FirstPage'

Vue.use(Vuex)
//设置cookie,增加到vue实例方便全局调用
//vue全局调用的理由是，有些组件所用到的接口可能需要session验证，session从cookie获取
//当然，如果session保存到vuex的话除外
Vue.prototype.setCookie = (c_name, value, expiredays) => {
  var exdate = new Date();　　　　
  exdate.setDate(exdate.getDate() + expiredays);　　　　
  document.cookie = c_name + "=" + escape(value) + ((expiredays == null) ? "" : ";expires=" + exdate.toGMTString());
}

//获取cookie、
function getCookie(name) {
  var arr, reg = new RegExp("(^| )" + name + "=([^;]*)(;|$)");
  if (arr = document.cookie.match(reg))
    return (arr[2]);
  else
    return null;
}
Vue.prototype.getCookie = getCookie;

//删除cookie
Vue.prototype.delCookie =(name) => {
    var exp = new Date();
    exp.setTime(exp.getTime() - 1);
    var cval = getCookie(name);
    if (cval != null)
      document.cookie = name + "=" + cval + ";expires=" + exp.toGMTString();
}

const store = new Vuex.Store({
  state: {
    logined: getCookie("session"),
  },
  mutations: {
    //更新用户信息
    login(state) {
      state.logined = true;
    },
    logout(state){
      state.logined = false;
    }
  }
})

export default {
  name: 'App',
  store:store,
  components: {
    firstPage,
  }
}


</script>

