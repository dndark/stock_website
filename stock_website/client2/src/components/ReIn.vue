<template>
  <div class="container">
    <div class="row">
      <div v-if="!hashVal" class="col-md-12">
        <h1>需重新入库</h1>
        
        
        <br>
        <b-table striped hover 
          :items="items" 
          :fields="fields"
          :per-page="perPage"
          :current-page="currentPage"
          >
          <template slot="id_number" slot-scope="data">
            <!-- `data.value` is the value after formatted by the Formatter -->
            <a :href="`#${data.item.id}`" @click="getProductInfo(data.item.id)">{{ data.item.id }}</a>
          </template>
          <template slot="pick_time" slot-scope="data">
            <!-- `data.value` is the value after formatted by the Formatter -->
            {{ dateFormat(data.item.pickupTime)}}
          </template>
          <template slot="button" slot-scope="data">
            <!-- `data.value` is the value after formatted by the Formatter -->
            <b-button class="btn-success" @click="reEnterToStock(data.item.id)">入库</b-button>
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
      <div v-else class="col-md-12">
        <h1> {{this.hashVal}} </h1>
        <b-table striped hover :items="productInfo" :fields="fields2">
        </b-table>
      </div>
    </div>
  </div>  
</template>

<script>

import common from '@/components/Common'
import axios from 'axios'

var ReIn = {
  name:"ReIn",
  data(){
    return {
      perPage: 8,
      currentPage: 1,
      items:[],
      fields: {
        id: {
          key: "id_number",
          label: '出库单号',
          formatter: 'fullName',
          sortable:true,

        },
        location: {
          label: '位置',
          sortable:true,

        },
        pickupTime:{
          key: "pick_time",
          label: '时间',
          sortable:true      ,
          // variant: 'warning'

        },
        button:{
          key: "button",
          label:'',

        }
      },
      productInfo:[],
      fields2: {
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
          label: '备注'        }
      },
    }
  },
  computed:{
    rows(){
      return this.items.length
    },
    hashVal() {
      // 我们很快就会看到 `params` 是什么
      return this.$route.hash.substring(1);
    }
  },
  methods:{
    reEnterToStock(id){
      
      var URL = this.site + "pendingDetail/" + id;
      axios.get(URL)
        .then((res) => {
          console.log(res.data)

          // window.location = "in/"
          // document.location = "in?action=DoThis";
          console.log(res.data)
          var r = {"amount":[], "itemID":[]};
          for (var x of res.data){
            r.amount.push(x.amount)
            r.itemID.push(x.itemID)
          }
          var queryString = this.ObjectToQueryString(r)
          // console.log(queryString)
          document.location = "in?"+queryString
        })
        .catch((error) => {
          console.log(error);
          
          document.location = "in?"
      });
    },
    getPendingItems(){
      var URL = this.site + "pendingLocations?isExpire=true";
      axios.get(URL)
        .then((res) => {
          this.items = res.data
        })
        .catch((error) => {
          console.log(error);
      });
    },
    getProductInfo(hashVal){
      var URL = this.site + "pendingDetail/" + hashVal;
      axios.get(URL)
        .then((res) => {
          this.productInfo = res.data
        })
        .catch((error) => {
          console.log(error);
      });
    },
  },
  created(){
    if (!this.hashVal){
      this.getPendingItems()
    }else{
      this.getProductInfo(this.hashVal)
    
    }
  },
  mixins: [common]
}
export default ReIn
</script>
