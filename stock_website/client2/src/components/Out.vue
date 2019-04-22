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
          <b-col  offset-md="2" md="auto">
            <select-out-state v-model="outState" class="float-right" ></select-out-state>
          </b-col >
          <b-col md="auto">
            <button id = "subButton" type="button" class="float-right btn btn-success btn-lg"  @click="submitOrder()">提交</button>
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
import VueDatepickerLocal from 'vue-datepicker-local'

var statDropDown = {
  name: "statDropDown",
  template:`
    <div>
      <div v-show="outState.state==='pending'" style="width: 15%;float: left;">
        提货时间：
      </div>
      <div v-show="outState.state==='pending'" style="width: 20%;float: left;margin: 0px 10px auto; ">
        <vue-datepicker-local 
        v-model="outState.pickupTime" 
        @change="update"
        ref='pickupTime'>
        </vue-datepicker-local>
      </div>
      <div v-show="outState.state==='pending'" style="width: 25%;float: left;margin: 0px 10px auto;">
        <b-form-input  
          placeholder="输入待出库位置" 
          v-model="outState.location"  
          @change="update"
          ref='locationVal'
        >
        </b-form-input>
      </div>
      <div :style=pendingStyle>
        <b-form-select 
          v-model="outState.state"
          :options="options"
          @change = "update"
          ref='optionsVal'
          >
        </b-form-select>
      
      </div>
  </div>
  `,
  data() {
    return{
      options:[
          { value: "pending", text: '待发货', pickupTime: '' },
          { value: 'out', text: '出库', pickupTime:''},
      ],
      outState: {
        state:"pending",
        location: "",
        // TODO may need to set different time value
        pickupTime: "",
      },
    }
  },
  computed:{
    preSetTime(){
      var d = new Date();
      d.setMonth(d.getMonth() + 3);
      return d 
    },
    pendingStyle(){
      if (this.outState.state==='pending') 
        return {
          width:'30%',
          float:'right'
        }
    }
  },
  methods: {
    update(){
      // pass value to parent
      this.outState.state = this.$refs.optionsVal.value
      this.outState.pickupTime = this.$refs.pickupTime.value
      this.outState.location = this.$refs.locationVal.value
      this.$emit('input',this.outState)
    }
  },
  components: {
    'VueDatepickerLocal': VueDatepickerLocal
  },
  created(){
    this.outState.pickupTime=this.preSetTime
  }
}

var Out = {
  name:"Out",
  data(){
    return {
      serialVal: "20171219-004CK",
      hasError:false,
      outState:{
        state:"pending",
        location:"",
        pickupTime:""
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
        stockNumber:{
          label: '库存数量',
        },
        amount: {
          label: '应出库数量',
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
    stockUpdatePayload(){
      var temp = JSON.parse(JSON.stringify(this.scanItems));
      for (var x of temp){
        x.stockNumber -= x.amount
      }
      return temp
    }
  },
  methods: {
    clearVal(){
      this.$refs.pathClear.value ='';
      this.hasError = false;
      this.fields.amount.label ='应出库数量';
      this.scanItems = [];
      this.items = [];
    },
    getSerialInfo(){
      // input check
      this.clearVal()
      if (this.serialVal.length == 0){
        window.alert("请输入出库单号");
        return 
      }
      
      var path = this.site +"out_item/"+ "out_code/" + this.serialVal
      axios.get(path)
        .then((res) => {
          this.updateItems(res.data)
        })
        .catch((error) => {
          console.log(error)
          window.alert("出库单号不存在")
      });
    },
    updateItems(resData){
      this.items = []
      for (var x of resData){
        for (var i=1; i <=5; i++){
          var item = {};
          var amount = 'out_item_number' + i;
          item["company"] = x['out_item_brand' + i]
          item["productType"] = x['out_item_name' + i]
          item["modelNumber"] = x['out_item_model' + i]
          item["info"] = x['out_item_parameter' + i]
          item["amount"] = x[amount]

          // make a copy of amount
          item["remain"] = x[amount]

          if (item.company != '' && item.modelNumber != '' ){
            this.items.push(item)
          }
        }
      }
    },
    
    loadInfo(itemID, number){
      const path = this.site + "item" + "/id/" + itemID
      axios.get(path)
        .then((res) => {
          // add the response data to importItems
          res.data["amount"] = number
          this.scanItems.push(res.data)
          this.crossingReference(res.data)
        })
        .catch((error) => {
          // eslint-disable-next-line
          this.hasError = true
          this.items.push({"id": itemID, "warning":"此产品未入库", _rowVariant: 'danger'})
          console.log(error)
        });
    },
    crossingReference(resData){
      // resData is the items in scandata and the amount is the number of time appear for each item
      let modelNumberClr = this.removeSpecialChar(resData.modelNumber);
      for (var x of this.items){
        // compare company name and model number to get match
        var xModelClr = this.removeSpecialChar(x.modelNumber);
        // if find match
        if (x.company == resData.company && xModelClr == modelNumberClr){
          x.remain = x.remain - resData.amount

          // manually update id AND stockNumber
          x.id = resData.id
          x.stockNumber = resData.stockNumber
          x.info = resData.info
          //todo 换成amount的值？？？？
          
          this.fields.amount.label = "实际出库数量"
          x.amount = resData.amount 

          this.warningMsg(x)
          return 
        }
      }
      // if not find match
      let item = JSON.parse(JSON.stringify(resData));
      this.items.push(item)
    },
    warningMsg(item){
      if (item.stockNumber < item.amount) return item.warning = "库房缺货"
      else if (item.remain > 0) return item.warning = "需要" + (item.remain+item.amount)+ ",缺" + item.remain +"个"
      else if (item.remain == 0) return item.warning = "√"
      else return item.warning = "需要" + (item.remain+item.amount)+ ",多" + Math.abs(item.remain) +"个"
    },
    rowClass(item) {
      if (!item) return 'table-danger'
      if (item.remain == item.amount) return 
      else if (item.stockNumber < item.amount) {this.hasError=true; return 'table-danger'}
      else if (item.remain == 0) return 'table-success'
      else if (item.remain < item.amount) return 'table-warning'
      else if (item.remain > item.amount) return 'table-warning'
      else return 'table-info'
    },
    updateStockInfo(){
      // update stock info
      var _self = this; 
      var URL = _self.site + "stocks/"
      _self.updateDate(_self.scanItems);
      axios.put(URL, _self.stockUpdatePayload)
        .then(() => {
          _self.dismissCountDown = _self.dismissSecs
        })
        .catch((error) => {
          console.log(error);
          window.alert("出库失败")
      });
    },
    submitOrder(){
      var _self = this;
      if (_self.hasError) return window.alert("有产品未入库 或者 库存缺货");
      
      var URL = _self.site + "pendingDetail/";
      var payload = {
          id: _self.serialVal,
          location: _self.outState.location,
          pickupTime: Date.parse(_self.outState.pickupTime),
          scanItems: _self.scanItems
      };
      _self.updateDate(_self.scanItems);
      

      // add to pending table
      if (_self.outState.state == "pending"){
        if (!_self.outState.location) return window.alert("请输入代发货货架号") 
        
        axios.post(URL, payload)
          .then(() => {
            console.log("pendingDetail Update")
            this.updateStockInfo()

          })
          .catch((error) => {
            console.log(error);
            window.alert("出库失败")
        });
        return 
      }else{
        this.updateStockInfo()
      }
    }
  },
  components: {
    'select-out-state': statDropDown,
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
