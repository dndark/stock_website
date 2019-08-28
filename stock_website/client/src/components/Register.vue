//register组件

<template>

<div class="register" id="register">
<br>
 <el-form :model="ruleForm" :rules="rules" ref="ruleForm" label-width="100px" class="demo-ruleForm">
  <el-form-item label="用户名" prop="username" >
   <el-input v-model="ruleForm.username" style="width:250px"></el-input>
  </el-form-item>
  <el-form-item label="密码" prop="pass">
   <el-input type="password" v-model="ruleForm.pass" auto-complete="off" style="width:250px"></el-input>
  </el-form-item>

  <el-form-item label="确认密码" prop="checkPass">
   <el-input type="password" v-model="ruleForm.checkPass" auto-complete="off" style="width:250px"></el-input>
  </el-form-item>

  <el-form-item label="您的名字" prop="name">
   <el-input  v-model="ruleForm.name" auto-complete="off" style="width:250px"></el-input>
  </el-form-item>
  <el-form-item>

   <el-button type="primary" @click="submitForm('ruleForm')">注册</el-button>
   <el-button @click="resetForm('ruleForm')">重置</el-button>
  </el-form-item>
 </el-form>

</div>
</template>

<script>

import common from '@/components/Common'

import axios from 'axios'
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms))
}

export default {
 data() {
  var validatePass = (rule, value, callback) => {
   if (value === '') {
    callback(new Error('请输入密码'));
   } else {
    if (this.ruleForm.checkPass !== '') {
     this.$refs.ruleForm.validateField('checkPass');
    }
    callback();
   }

  };
  var validatePass2 = (rule, value, callback) => {
   if (value === '') {
    callback(new Error('请再次输入密码'));
   } else if (value !== this.ruleForm.pass) {
    callback(new Error('两次输入密码不一致!'));
   } else {
    callback();
   }
  };

  return {
   activeName: 'second',
   ruleForm: {
    name: '',
    username: '',
    pass: '',
    checkPass: '',
   },
   rules: {
    name: [
    { required: true, min: 2, max: 15, message: '长度在 2 到 15 个字符', trigger: 'blur' }
    ],
    username: [
     { required: true, message: '请输入您的用户名', trigger: 'blur' },
     { min: 2, max: 15, message: '长度在 2 到 15 个字符', trigger: 'blur' }
    ],
    pass: [
     { required: true, validator: validatePass, trigger: 'blur' }
    ],
    checkPass: [
     { required: true, validator: validatePass2, trigger: 'blur' }
    ],
   }
  };
 },

 methods: {
  submitForm(formName) {
   this.$refs[formName].validate((valid) => {
    if (valid) {
        // sleep 1000 sec, than change page
        
        var self = this;
        (async function() {
            
            let payload = {"username":self.ruleForm.username, "password":self.ruleForm.pass, "name":self.ruleForm.name}
            let path = self.site+'/Register'
            axios.post(path, payload)
            .then((res) => {
                if (res.data.register_status == true){
                    self.$message({
                        type: 'success',
                        message: '注册成功',
                        duration: 800
                    });
                    sleep(1500)
                    self.$router.push('/login');
                }
                else{
                    self.$message({
                        type: 'fail',
                        message: res.data.message,
                    });
                }
            })
        })()
 
    } else {
     console.log('error submit!!');
     return false;
    }
   });
  },
  resetForm(formName) {
   this.$refs[formName].resetFields();
  }
 },
  mixins: [common],
}

</script>

<style scoped>
.register{position: fixed; overflow: hidden;left: 50%; margin-left: -250px; top:60%; margin-top: -350px; width: 500px; min-height: 555px; z-index: 10; right: 140px; background: #fff;-webkit-border-radius: 5px;
-moz-border-radius: 5px;
-ms-border-radius: 5px;
-o-border-radius: 5px;
border-radius: 5px; -webkit-box-shadow:  0px 3px 16px -5px #070707; box-shadow:  0px 3px 16px -5px #070707}

</style>