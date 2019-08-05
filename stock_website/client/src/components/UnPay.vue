<template>
  <div class="container">
    <div class="row">
      <div class="col-md-12">
        <h1 style="color: red"><b>未付款</b></h1>

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
  computed:{
    // nameOptions2(){
    //   var newList = [{value:"所有人", text:"所有人("+this.items.length+")"}]
    //   for (var x of this.nameOptions){
    //     if (x.name != "所有人"){
    //       var countNumberOfName = this.items.filter(item => item.sc_sponsor === x.value).length;
    //       newList.push({value:x.value, text:x.text+"("+countNumberOfName+")"})
    //     }
    //   }
    //   return newList
    // }
  },
  methods:{
    getItems(options){
      var url = this.site + "unPayItems?";
      var options = options||{}
      if ("year" in options){url += 'year='+options.year+"&"}
      if ("name" in options){url += 'name='+options.name+"&"}

      self = this
      axios.get(url)
        .then((res) => {
          self.items = res.data
          self.currentPage = 1
          if (self.onceItems.length == 0){
            self.onceItems = JSON.parse(JSON.stringify(res.data));
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
      this.getItems({year:this.yearSelected, name:this.nameSelected })
    },
  },
  created(){
    this.getItems()
  },
  mixins: [UnpayCommon]
}
export default UnPay
</script>
