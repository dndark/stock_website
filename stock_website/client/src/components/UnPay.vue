<template>
  <div class="container">
    <div class="row">
      <div class="col-md-12">
        <h1 style="color: red">未付款</h1>

        <b-container class="bv-example-row">
            <b-row>
                <b-col>             
                    <p>年份:</p>
                    <b-form-select v-model="yearSelected" :options="yearOptions" @change=reloadItem class="col-md-5"></b-form-select>
                </b-col>
                <b-col>
                    <p>姓名:</p>
                    <b-form-select v-model="nameSelected" :options="nameOptions2" @change=reloadItem class="col-md-5"></b-form-select>
                </b-col>
            </b-row>
        </b-container>
        <br>
        <b-table striped hover 
          :items="items" 
          :fields="fields"
          :per-page="perPage"
          :current-page="currentPage"
          :fixed= true
          :small= true
          :outlined = true
          :sort-compare="sortDate"
          >
          <template slot="sc_code" slot-scope="data" >
              <a :title="data.item.sc_code" :href="'unPayDetail?sc_code='+data.item.sc_code">
                {{data.item.sc_code.slice(0,18) }}
              </a>
          </template>
          <template slot="sc_appd_date" slot-scope="data" >
            {{ dateFormat(data.item.sc_appd_date) }}
          </template>
          <template slot="sc_receive_company" slot-scope="data" >
            <span :title="data.item.sc_receive_company">{{ data.item.sc_receive_company.slice(0,15) }}</span>
          </template>  
          <template slot="sc_rec_money" slot-scope="data">
            {{ numFormat(data.item.sc_rec_money) }}
          </template>
          <template slot="sc_recr_money_prec" slot-scope="data">
            {{ precentFormat(data.item.sc_recr_money_prec * 100)}}
          </template> 
          <template slot="sc_item_in" slot-scope="data">
            {{ precentFormat(data.item.sc_item_in)}}
          </template>
          <template slot="sc_item_out" slot-scope="data">
            {{ precentFormat(data.item.sc_item_out) }}
          </template>
          <template slot="handle" slot-scope="data">
            <input type="checkbox" v-model="data.item.handle" v-on:click="postUpdateItem(data.item)">
          </template>
        </b-table>
        <div class="overflow-auto">
            <b-pagination
              align="fill"
              v-model="currentPage"
              :total-rows="rows"
              :per-page="perPage"
              aria-controls=""
            />
        </div>
      </div>
    </div>
  </div>  
</template>

<script>

import UnpayCommon from '@/components/UnpayCommon' 
import axios from 'axios'

var UnPay = {
  name:"UnPay",
  data(){
    return {
      fields: {
        id: {
          key: "sc_code",
          label: '合同编号',
        },
        appd_date:{
          key: "sc_appd_date",
          label: '交货期',
          sortable:true,
        },
        company: {
          key: "sc_receive_company",
          label: '客户单位名称',
          sortable:true,
        },
        recr_money_prec:{
          key: "sc_recr_money_prec",
          label: '收款情况',
          sortable:true,
        },
        item_summoney:{
          key: "sc_item_summoney",
          label:'销售金额',
          sortable:true,
        },
        sponsor:{
          key: "sc_sponsor",
          label:'主管人',
          sortable:true,
        },
        handle:{
          key: "handle",
          label:'已处理'
        },
      },
    }
  },
  methods:{
    getItems(){
      var url = this.site + "unPayItems?";
      url += 'year='+this.yearSelected+"&" + 'name='+this.nameSelected

      var self = this
      axios.get(url)
        .then((res) => {
          self.items = res.data
          self.currentPage = 1
          // onceItem need to be corresponding to the correct year, so if nameSelected 
          // is all, we could just copy the res.data obj to onceItems. if the nameSelected
          // is not the all, we need to make one more extract API call, to fetch all user information
          // this may cause redundant call
          if (self.nameSelected == "所有人"){
            self.onceItems = JSON.parse(JSON.stringify(res.data));
          }else{
            url = url.replace(self.nameSelected,"所有人")
            axios.get(url).then((res)=>{self.onceItems = JSON.parse(JSON.stringify(res.data));})
          }
          
        })
        .catch((error) => {
          console.log(error);
      });
    },
    // this function call API and update the database
    postUpdateItem(value){
      var url = this.site + "updateUnPayItem";
      var self = this
      axios.post(url,{
          handle_score: 10,        
          sc_code: value.sc_code  
        })
        .then((res) => {
          // deleted the item from page
          let index = self.items.findIndex(item => item.sc_code ===  value.sc_code) // find the post index 
          if (index != -1){
            self.items[index].handle = false
            self.items.splice(index, 1) //delete the post
          }
          // deleted the item from onceItem
          index = self.onceItems.findIndex(item => item.sc_code ===  value.sc_code) // find the post index 
          if (index != -1){
            self.onceItems.splice(index, 1) 
          }
        })
        .catch((error) => {
          console.log(error);
      });
    },
    reloadItem(value){
      this.getItems()
    },
  },
  // created(){
  //   this.getItems()
  // },
  mixins: [UnpayCommon]
}
export default UnPay
</script>

<style scoped>
</style>
