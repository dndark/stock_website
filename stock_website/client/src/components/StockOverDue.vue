<template>
  <div class="container">
    <div class="row">
      <div class="col-md-12">
        <h1>销售合同</h1>

        <p>日期：{{ this.today}}   </p>
        <p>货物已经全部入库，提货期超过三个月还未提货的销售合同</p>
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
          <template slot="sc_appd_date" slot-scope="data" >
            {{ dateFormat(data.item.sc_appd_date) }}
          </template>
          <template slot="sc_recr_money_prec" slot-scope="data">
            {{ data.item.sc_recr_money_prec * 100 + "%"}}
          </template>
          <template slot="sc_item_in" slot-scope="data">
            {{ data.item.sc_item_in + "%" }}
          </template>
          <template slot="sc_item_out" slot-scope="data">
            {{ data.item.sc_item_out + "%" }}
          </template>
        </b-table>
        <div class="overflow-auto">
            <b-pagination
              align="fill"
              v-model="currentPage"
              :total-rows="rows"
              :per-page="perPage"
              aria-controls=" "
            />
        </div>
      </div>
    </div>
  </div>  
</template>

<script>

import common from '@/components/Common'
import axios from 'axios'

var StockOverDue = {
  name:"StockOverDue",
  data(){
    return {
      perPage: 15,
      currentPage: 1,
      items:[],
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
        rec_money:{
          key: "sc_rec_money",
          label:'已收金额',
          sortable:true,
        },
        item_summoney:{
          key: "sc_item_summoney",
          label:'销售金额',
          sortable:true,
        },
        item_in:{
          key: "sc_item_in",
          label:'入库',
          sortable:true,
        },
        item_out:{
          key: "sc_item_out",
          label:'出库',
          sortable:true,
        },
        sponsor:{
          key: "sc_sponsor",
          label:'主管人',
          sortable:true,
        }
      },
    }
  },
  computed:{
    rows(){
      return this.items.length
    },
    today(){
      return this.dateFormat(new Date())
    }
  },
  methods:{
    getItems(){
      var URL = this.site + "OverDueItem";
      axios.get(URL)
        .then((res) => {
          this.items = res.data
        })
        .catch((error) => {
          console.log(error);
      });
    },
    toString(value) {
      if (!value) {
        return ''
      } else if (value instanceof Object) {
        return keys(value)
          .sort()
          .map(key => toString(value[key]))
          .join(' ')
      }
      return String(value)
    },  
    sortDate(a, b, key) {
      if (typeof a[key] === 'number' && typeof b[key] === 'number') {
        // If both compared fields are native numbers
        return a[key] < b[key] ? -1 : a[key] > b[key] ? 1 : 0
      } else if (key == 'sc_appd_date') {
        if (new Date(a[key]) < new Date(b[key])) return 1;
        if (new Date(a[key]) > new Date(b[key])) return -1;
      } else{
        return this.toString(a[key]).localeCompare(this.toString(b[key]), undefined, {
          numeric: true
        })
      }
    },
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
  },
  created(){
    this.getItems()
  },
  mixins: [common]
}
export default StockOverDue
</script>
