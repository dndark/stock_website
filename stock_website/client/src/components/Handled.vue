<template>
  <div class="container">
    <div class="row">
      <div class="col-md-12">
        <h1 style="color: #00FF99"><b>已处理</b></h1>

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
          <template slot="last_modified_date" slot-scope="data">
            {{ dateFormat2(data.item.last_modified_date) }}
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

var Handled = {
  name:"Handled",
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
        last_modified_date:{
          key: "last_modified_date",
          label:'处理日期',
          sortable:true,
        }
      },
    }
  },
  methods:{
    getItems(options){
      var url = this.site + "unPayItems?";
      var options = options||{}
      if ("year" in options){url += 'year='+options.year+"&"}
      if ("name" in options){url += 'name='+options.name+"&"}
      url += "handled=yes&"
      
      self = this
      axios.get(url)
        .then((res) => {
          self.items = res.data
          self.currentPage = 1
        })
        .catch((error) => {
          console.log(error);
      });
    },
    reloadItem(value){
      this.getItems({year:this.yearSelected, name:this.nameSelected })
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
  },
  created(){
    this.getItems()
  },
  mixins: [UnpayCommon]
}
export default Handled
</script>
