<template>
  <div class="container">
    <div class="row">
      <div class="col-md-12">
        <h1>出库</h1>
        <hr><br>
          <div class="form-group">
            <b-container class="b-container" fluid>
                <b-row>
                    <b-col sm="2">
                        <label for="input-serial">出库单号:</label>
                    </b-col>
                    <b-col sm="3">
                        <b-form-input id="input-serial" size="md" placeholder="输入出库单号" v-model="serialVal"></b-form-input>
                    </b-col>
                    <b-col sm="2" >
                       <b-button class="btn-md btn-circle" variant="success" @click="getSerialInfo()">查找</b-button>
                    </b-col>
                    <b-col sm="2" offset-sm="1">
                      
                      <b-alert
                        :show="dismissCountDown"
                        fade
                        variant="success"
                        @dismissed="dismissCountDown=0"
                        class = "alert"
                      >
                        成功出库
                      </b-alert>
                    </b-col>
                    <b-col md="2">
                        <label class="btn btn-info">
                            导入出库列表 <input type="file" ref="pathClear" @change="readFile" hidden>
                        </label>
                    </b-col>
                </b-row>
            </b-container>
          </div>
        <b-table striped hover :items="items" :tbody-tr-class="rowClass" :fields="fields"></b-table>
      <b-container class="b-container" fluid>
        <b-row align-h="end">
          <b-col offset-md = "7"  md="auto">
            <select-out-state v-model="outState" class="float-right" ></select-out-state>
          </b-col >
          <b-col md="auto">
            <button id = "subButton" type="button" class="float-right  btn btn-success btn-lg"  @click="submitOrder()">提交</button>
          </b-col>
        </b-row>
      </b-container>       
      </div>
      
    </div>
   
  </div>
</template>

<script>

import axios from 'axios'
import common from '@/components/Common'
var statDropDown = {
  name: "statDropDown",
  template:`
    <div>
      <div v-if="outState.state==='pending'" style="width:50%; float:left">
        <b-form-input  placeholder="输入待出库位置" :value="outState.location" @input="updateLocation"></b-form-input>
      </div>
      <div :style=pendingStyle>
        <b-form-select 
          v-model="outState.state"
          :options="options"
          @change = "selectState"
          >
        </b-form-select>
      
      </div>
  </div>
  `,
  data() {
    return{
      options:[
          { value: "pending", text: '待发货' },
          { value: 'out', text: '出库' },
      ],
      outState: {
                  state:"pending",
                  location: "",
                }
    }
  },
  computed:{
    pendingStyle(){
      if (this.outState.state==='pending') 
        return {
          width:'40%',
          float:'right'
        }
    }
  },
  methods: {
    selectState(e){
      this.outState.state = e
      this.$emit('input',this.outState)
    },
    updateLocation(e){
      this.outState.location = e
      this.$emit('input',this.outState)
    }
  }
}

var Out = {
  name:"Out",
  data(){
    return {
      serialVal: "20171219-004CK",
      serialResponse: [],
      hasError:false,
      outState:{
        state:"pending"
      },
      fields: {
            id: {
              label: '条纹码'
            },
            productType: {
              label: '种类',
              sortable:true
            },
            company: {
              label: '厂家',
              sortable:true
            },
            modelNumber: {
              label: '型号',
              sortable:true
            },
            amount: {
              label: '数量',
              sortable:true
            },
            info: {
              label: '备注'
            },
            warning:{
              label: '提示'
            }
      },
      items: [],
      scanItems: []
    }
  },
  computed:{
    clearVal(){
      this.$refs.pathClear.value =''
      this.error = false
    },
  },
  methods: {
    getSerialInfo(){
      // input check
      this.clearVal
      if (this.serialVal.length == 0){
        window.alert("请输入出库单号");
        return 
      }
      
      var path = this.site +"out_item/"
      path = path + "out_code/" + this.serialVal
      axios.get(path)
        .then((res) => {
          console.log(res)
          this.updateItems(res.data)
        })
        .catch((error) => {
          window.alert("出库单号不存在")
      });
    },
    updateItems(resData){
      this.items = []
      for (var x of resData){
        for (var i=1; i <= 5; i++){
          const item = {} 
          var amount = 'out_item_number' + i;
          var info = 'out_item_parameter' + i;
          var productType = 'out_item_name' + i;
          var modelNumber = 'out_item_model' + i;
          var company = 'out_item_brand' + i; 
          
          item["company"] = x[company]
          item["productType"] = x[productType]
          item["modelNumber"] = x[modelNumber]
          item["amount"] = x[amount]
          item["info"] = x[info]
          // for compare with out stock
          item.remain = x[amount]
          if (item.company != '' && item.modelNumber != '' ){
            this.items.push(item)
          }
        }
      }
    },
    
    loadInfo(itemID, arr){
      const path = this.site + "item" + "/id/" + itemID
      axios.get(path)
        .then((res) => {
            // add the response data to importItems
            res.data.stockNumber -= arr[itemID]
            this.scanItems.push(res.data)
            
            this.crossingReference(res.data, arr[itemID])
        })
        .catch((error) => {
        // eslint-disable-next-line
          this.hasError = true
          this.items.push({"id": itemID, "warning":"此产品未入库", _rowVariant: 'danger'})
        });
    },
    crossingReference(resData, amount){
      const modelNumberClr = this.removeSpecialChar(resData.modelNumber);
      for (var x of this.items){
        // compare company name and model number to get match
        var xModelClr = this.removeSpecialChar(x.modelNumber);
        // if find match
        if (x.company == resData.company && xModelClr == modelNumberClr){
          x.remain = x.remain - amount
          x.id = resData.id
          if (x.remain > 0){
            x.warning = "缺" + x.remain +"个货"
          }
          else{
            x.warning = "√"
          }
          return 
        }
      }
      // if not find match
      let item = {};
      item.id = resData.id
      item.company = resData.company
      item.productType = resData.productType
      item.modelNumber = resData.modelNumber
      item.amount = amount
      this.items.push(item)
    },
    rowClass(item, type) {
      if (!item) return
      if (item.remain == item.amount) return 
      else if (item.remain == 0) return 'table-success'
      else if (item.remain < item.amount) return 'table-warning'
      else return 'table-info'
    },
    submitOrder(){
      if (this.hasError) return window.alert("有没入库的产品") 
      
      var path = this.site +"stocks/"
      var payload = this.scanItems
      this.updateDate()
      axios.put(path, payload)
        .then(() => {
          this.dismissCountDown = this.dismissSecs
        })
        .catch((error) => {
        console.log(error);
      });
      
    }
  },
  components: {
    'selectOutState': statDropDown,
  },
  mixins: [common]
}

export default Out
</script>



<style>
  #itemNumberID {
    width:10ch
  }
  #delButton {
    margin-top: 1ch
  }
  [hidden] {
    display: none !important;
  }
</style>
