<template>
  <div class="container">
    <div class="row">
      <div class="col-md-12" v-if='!this.$route.query.sc_code'>
          <b-row>
            <b-col class="col-md-2 text-right">
              输入合同号：
            </b-col>
            <b-col class="col-md-4">
              <b-form-input v-model="searchText" placeholder="Search"></b-form-input>
            </b-col>
            <b-col offset-md="4" class="col-md-1">
              <b-button  variant="outline-success" type="submit" v-on:click="search()" >Search</b-button>
            </b-col>
          </b-row>
          <br>
      </div>
    
      <div class="col-md-12" v-if='this.sc_code'>
        
        <div v-if="this.no_data">找不到结果</div>
        <div v-else>
          <h1 style="margin-bottom: 20px; text-align:center" >合同明细</h1>

          <b-container class="bv-example-row">
            <div v-for="(value, name) in processItem" :key=name>
              <b-row  style="margin-bottom: 10px">
                <b-col cols="7">{{name}}</b-col>
                <b-col cols="5" style="word-wrap:break-word; white-space: pre-line;">{{value}}</b-col>
              </b-row>
            </div>
            <div class="state" v-show="this.isAdmin">
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
            </div>
        </b-container>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import UnpayCommon from '@/components/UnpayCommon'
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
      remark:'',
      searchText:'',
      sc_code:this.$route.query.sc_code,
      no_data: false
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
      var url = this.site + "unPayItem?sc_code="+ this.sc_code ;
      var self = this
      axios.get(url)
        .then((res) => {
          
          this.no_data = false
          self.item = res.data
        })
        .catch((error) => {
              if (error.response || error.request) {
                // The request was made and the server responded with a status code
                // that falls out of the range of 2xx
                this.no_data = true
              } 
      });
    },
    submit(){
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
      });
    },
    search(){
      let url = window.location.href
      url = url +"?sc_code=" + this.searchText
      this.sc_code =  this.searchText
      this.getItem()
      return 
    },
  },
  created(){
    this.getItem()
  },
  mixins: [UnpayCommon]
}
export default UnPayDetail
</script>

