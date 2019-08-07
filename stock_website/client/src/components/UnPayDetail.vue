<template>
  <div class="container">
    <div class="row">
      <div class="col-md-12">
        <h1 style="margin-bottom: 20px; text-align:center" >合同明细</h1>

        <b-container class="bv-example-row">
          <div v-for="(value, name) in processItem" :key=name>
            <b-row  style="margin-bottom: 10px">
              <b-col cols="7">{{name}}</b-col>
              <b-col cols="5" style="word-wrap:break-word; white-space: pre-line;">{{value}}</b-col>
            </b-row>
          </div>
          <b-row style="margin-bottom:10px" variant="success">
              <b-col cols="7">处理状态</b-col>
              <b-col cols="2">
                <b-form-select v-model="selected">
                  <option v-for="option in options" v-bind:value="option.value" :key='option.name'> {{ option.text }}</option>
                </b-form-select>
                </b-col>
            </b-row>
            <b-row style="margin-bottom: 10px" variant="success" >
              <b-col cols="7">备注</b-col>
              <b-col cols="5">
                    <b-form-input v-model="remark"></b-form-input>
              </b-col>
            </b-row>
            <b-col offset-md="11" style="margin-top:40px">
              <b-button size="lg" variant="success"  v-on:click="submit()">提交</b-button>
            </b-col>
        </b-container>
      </div>
    </div>
  </div>
</template>

<script>
import common from '@/components/Common'
import axios from 'axios'

var UnPayDetail = {
  name:"UnPayDetail",
  data(){
    return {
      item: {},
      options:[
        { value: "progress", text:'处理中'},
        { value: "handled", text:'已处理'},
      ],
      selected: "progress",
      remark:''
    }
  },
  computed:{
    processItem(){
      var obj = {}
      obj["合同编号"] = this.item.sc_code
      obj["交货期"] = this.dateFormat(this.item.sc_appd_date)
      obj["入库"] = this.precentFormat(this.item.sc_item_in)
      obj["出库"] = this.precentFormat(this.item.sc_item_out) 
      obj["主管人"]= this.item.sc_sponsor
      obj["销售金额"] = this.numFormat(this.item.sc_item_summoney)
      obj["已收金额"] = this.numFormat(this.item.sc_rec_money)
      obj["已收金额比例"] = this.precentFormat(this.item.sc_recr_money_prec)
      obj["客户单位名称"] = this.item.sc_receive_company 
      
      let str = this.item.remark
      
      obj["旧备注"] = str
      if (str){
        obj["最后处理时间"] = this.dateFormat2(this.item.last_modified_date)
      }
      return obj
    }
  },
  methods:{
    
    dateFormat(t){
      // var dateNum =  Date.parse(t);
      if (t){
          var dateObj = new Date(t);
          var month = dateObj.getUTCMonth() + 1; //months from 1-12
          var day = dateObj.getUTCDate();
          var year = dateObj.getUTCFullYear();
          return  year + "/" + month + "/" + day;
      }
      return ''
    },
    dateFormat2(t){
      // var dateNum =  Date.parse(t);
      if (t){
          var dateObj = new Date(Number(t));
          var month = dateObj.getUTCMonth() + 1; //months from 1-12
          var day = dateObj.getUTCDate();
          var year = dateObj.getUTCFullYear();
          var hour = dateObj.getUTCHours();
          var min = dateObj.getUTCMinutes();
          return  year + "/" + month + "/" + day + " " +hour+":"+min;
      }
      return ''
    },
    getItem(){
      var sc_code = this.$route.query.sc_code
      console.log(sc_code)
      var url = this.site + "unPayItem?sc_code="+ sc_code ;
      var self = this
      axios.get(url)
        .then((res) => {
          self.item = res.data
          console.log(self.item)
          // self.currentPage = 1
        })
        .catch((error) => {
          console.log(error);
      });
    },
    submit(){
      console.log(this.selected)
      
      var today = this.dateFormat(new Date())
      var remark = '';
      var score = 0;
      var url = this.site + "updateUnPayItem";

      if (this.remark){
        remark = today+":"+this.remark+"\n\n"
      }
      if (this.selected == "handled"){
        score = 10
      }else if(this.selected == "progress"){
        score = 5
      }
      console.log(remark)
      var self = this
      axios.post(url,{
          remark: remark,
          handle_score: score,
          sc_code: self.item.sc_code,   
        })
        .then((res) => {
          alert("已经提交")
          window.location.reload()
        })
        .catch((error) => {
          alert("提交失败")
          console.log(error);
      });
    }
  },
  created(){
    console.log(123)
    this.getItem()
  },
  mixins: [common]
}
export default UnPayDetail
</script>

