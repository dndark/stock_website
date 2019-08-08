<template>
  <div class="container">
    <div class="row">
      <div class="col-md-12">
        <h1>新货输入</h1>
        <hr><br>
        
        <label class="btn btn-info">
            导入表格 <input type="file" @change="readFile2" hidden>
        </label>
        <table class="table table-hover">
          <thead>
            <tr>
              <th></th>
              <th scope="col">条纹码</th>
              <th scope="col">种类</th>
              <th scope="col">厂家</th>
              <th scope="col">型号</th>
              <th scope="col">备注</th>
              <!-- <th scope="col">库存总数</th> -->
              <th scope="col">位置</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <!-- <tr -->
            <tr v-if="items.length == 0">
              <td><b-button class="btn-sm btn-circle" variant="success" @click="newRow">+</b-button></td>
            </tr>
            <tr v-else v-for="(item, index) in items" :key="index" >
              
              <td><b-button class="btn-sm btn-circle" variant="success" @click="newRow">+</b-button></td>
              <!-- <td><b-form-input class="input-lg" type="text" v-model="item.id" ></b-form-input></td>
              <td><b-form-input class="input-lg" type="text" v-model="item.company"></b-form-input></td>
              <td><b-form-input class="input-lg" type="text" v-model="item.modelNumber"></b-form-input></td>
              <td><b-form-input class="input-md" type="text" v-model="item.info"></b-form-input></td>
              <td><b-form-input class="input-md" type="text" v-model="item.location"></b-form-input></td> -->
              <td> <b-form-textarea size="sm"  rows=1 max-rows=4 v-model="item.id"></b-form-textarea></td>
              <td> <b-form-textarea class="textA" size="sm"  min-rows="1" max-rows="4" v-model.trim="item.type"></b-form-textarea></td> 
              <td> <b-form-textarea class="textA" size="sm"  min-rows="1" max-rows="4" v-model.trim="item.company"></b-form-textarea></td>
              <td> <b-form-textarea class="textA" size="sm"  min-rows="1" max-rows="4" v-model.trim="item.modelNumber"></b-form-textarea></td>
              <td> <b-form-textarea class="textA" size="sm"  min-rows="1" max-rows="4" v-model.trim="item.info"></b-form-textarea></td>
              <td> <b-form-textarea class="textA" size="sm"  min-rows="1" max-rows="4" v-model.trim="item.location"></b-form-textarea></td>
              
              <td><b-button class="btn-sm btn-circle" variant="danger" @click="deletedItem(item)">-</b-button></td>
              
            </tr>
            
          </tbody>
        </table>
        <button id = "delButton" type="button" class="float-right btn btn-success btn-lg"  @click="submitOrder()">提交</button>
             
      </div>
      
    </div>
   
  </div>
</template>

<script>

import common from '@/components/Common'
import axios from 'axios'

export default {
  name:"new",
  data(){
    return{
      // nRow:[1],
      items:[
        {
          key: "this is a unique key",
          id:'',
          company:'',
          modelNumber:'',
          productType:'',
          info:'',
          number:0,
          location:'',
          lastModifiedDate: Date.now()
        }
      ],
    }
  },
  computed:{
    uuidv4() {
      return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16);
      });
    }
  },
  methods: {
    newRow(){
      //  this.n = this.n+1
      //  this.nRow.push(this.n)
       this.items.push({
          key: this.uuidv4,
          id:'',
          company:'',
          modelNumber:'',
          productType:'',
          info:'',
          number:0,
          location:'',
          lastModifiedDate: Date.now()
        })
    },
    deletedItem(item){
      var a = this.items.indexOf(item);
      this.items.splice(a,1)
    },
    validID(){
      var idArray = [];
      for (var value of this.items) {
        // check if the id is empty
        if (value.id.length == 0){
          return false
        }

        // check if the id is duplicate
        if (idArray.indexOf(value.id) != -1){
          return false
        }else{
          idArray.push(value.id)
        }
      }
      return true
    },
    validObj(obj){
      if (!obj) return false
      else return true
    },
    validOrder(){
      var errMsg;
      if (!this.validID()){
        errMsg = "条纹码重复或者为空";
        return [false, errMsg];
      }
      for (var value of this.items) { 
        if (!this.validObj(value.company)){
          errMsg = "公司不能为空";
          return [false, errMsg];
        }
        if (!this.validObj(value.modelNumber)){
          errMsg = "型号不能为空";
          return [false, errMsg];
        }
        if (!this.validObj(value.location)){
          errMsg = "位置不能为空";
          return [false, errMsg];
        }
      }
      return [true,errMsg];
    },
    submitOrder(){
      // for (var i=0; i<this.nRow.length; i++){
        
      var _this = window;
      if (this.validOrder()[0] == false){
        alert(this.validOrder()[1])
        return
      }
      var path = this.site +"stocks/"
      var payload = this.items
      axios.post(path, payload)
        .then(() => {
           window.alert("成功导入新货")
          _this.location.reload()
        })
        .catch((error) => {
           window.alert(error);
        });
    },
    loadInfo(itemID, arr){
      const path = this.site + "item" + "/id/" + itemID
      axios.get(path)
        .then((res) => {
        })
        .catch((error) => {
          var item = {"id":itemID, 
                      company:'',
                      modelNumber:'',
                      productType:'',
                      info:'',
                      number:0,
                      location:'',
                      lastModifiedDate: Date.now()}
          this.items.push(item);
        });
    },
    readFile2(e){
      this.items = []
      this.readFile(e)
    }
    
  },
  mixins: [common],
}
</script>


<style>
  #itemNumberID {
    height:auto;
  }
  .btn-circle {
    width: 30px;
    height: 30px;
    text-align: center;
    padding: 6px 0;
    font-size: 12px;
    /* line-height: 1.42; */
    border-radius: 15px;
  }

  .input-lg{
    width:150px
  }

  .input-md{
    width:100px
  }

  .input-sm {
    width:50px
  }

  .textA {
    height: 40px
  }
  
</style>
