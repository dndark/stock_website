<template>
  <div class="container">
    <div class="row">
      <div class="col-md-12">
        <h1>入库</h1>
        <hr><br>
          <div class="form-group">
            <label class="btn btn-info">
                导入表格 <input type="file" @change="readFile" hidden>
            </label>
              <b-alert
                :show="dismissCountDown"
                fade
                variant="success"
                @dismissed="dismissCountDown=0"
                class = "alert"
              >
                成功输入
              </b-alert>
          </div>
        <!-- <br><br> -->
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">条纹码</th>
              <th scope="col">种类</th>
              <th scope="col">厂家</th>
              <th scope="col">型号</th>
              <th scope="col">日期</th>
              <th scope="col">备注</th>
              <th scope="col"  title="双击修改">新增个数</th>
              <th scope="col" >库存总数</th>
              <th scope="col"  title="双击修改">位置</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <!-- <tr> -->
              <tr v-for="(item, index) in items" :key="index">
                <td>{{ item.id }}</td>
                <td>{{ item.productType }}</td>
                <td>{{ item.company }}</td>
                <td>{{ item.modelNumber }}</td>
                <td>{{ dateFormat(item.lastModifiedDate) }}</td>
                <td>{{ item.info }}</td>
                <td>
                  <span v-if="!editing" @dblclick="edit">{{item.number}}</span>
                  <input 
                  v-else
                  id="itemNumberID" 
                  type="number"
                  min="0"
                  ref="input" 
                  
                  v-model.number="item.number"
                  @keyup.enter = "save"
                  @blur="save">
                <!-- <td></td> -->
                <td>{{ numberTotal(item) }}</td>
                <td @dblclick="editLocation"> 
                  <span  style="min-width: 20px" v-if="!editingLocation" >{{item.location}}</span>
                  <input 
                  id="itemLocationID" 
                  ref="input" 
                  v-if="editingLocation"
                  @keyup.enter = "saveLocation"
                  v-model.number="item.location"
                  @blur="saveLocation">
                </td>
                  <!-- <button type="button" class="btn btn-warning btn-sm">Update</button> -->
                <button id = "delButton" type="button" class="btn btn-danger btn-sm"  @click="onDeleteitem(item)">删除</button>
                
            </tr>
          </tbody>
        </table>
        
      <button id = "subButton" type="button" class="float-right btn btn-success btn-lg" @click="submitOrder()">提交</button>
             
      </div>
      
    </div>
   
  </div>
</template>

<script>

import axios from 'axios'
import common from '@/components/Common'

var In = {
  name:"In",
  data(){
    return {
      editing:false,
      editingLocation:false,
      items:[],
    }
  },
  computed:{
    parseURLQuery(){
      var items = this.QueryStringToObject();
      if (items && items.itemID){
        for (var i =0; i < items.itemID.length; i++){
          var id = items.itemID[i];
          var number = items.amount[i];
          this.loadInfo(id, number);
        }
      }
    }
  },
  methods: {
    onDeleteitem(selectItem) {
      var a = this.items.indexOf(selectItem);
      this.items.splice(a, 1);
    },
    edit() {
      this.editing = true
    },
    save() {
      this.editing = false
    },
    editLocation(){
      this.editingLocation = true
    },
    saveLocation(){
      this.editingLocation = false
    },
    
    numberTotal(selectItem){
      
      let numOfItemInStock = selectItem.stockNumberTemp;
      
      let total = Number(selectItem.number) + numOfItemInStock
      if (selectItem.number > 0 ){
        selectItem.stockNumber = total
        return selectItem.number + " + " + numOfItemInStock + " = " + String(total)
      }
      return numOfItemInStock
    },
    loadInfo(itemID, number){
      let path = this.site + "item" + "/id/" + itemID
      axios.get(path)
        .then((res) => {
            res.data.number = number
            // tempory solution, TODO, I want to modified a stockNumber without realtime display
            res.data.stockNumberTemp = res.data.stockNumber
            this.items.push(res.data);
        })
        .catch((error) => {
        // eslint-disable-next-line
          console.error(error);
        });
    },
    submitOrder (){
      var path = this.site +"stocks/"
      var payload = this.items
      this.updateDate(payload)
      axios.put(path, payload)
        .then(() => {
          this.dismissCountDown = this.dismissSecs
        })
        .catch((error) => {
      });
    },
    
  },
  created(){
    this.parseURLQuery
  },
  mixins: [common]
}

export default In
</script>


<style>
  #itemNumberID,#itemLocationID {
    width:10ch
  }
  #delButton {
    margin-top: 1ch
  }
  [hidden] {
    display: none !important;
  }

  .alert {
    width:20%;
    float:right
  }
</style>
