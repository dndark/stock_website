<template>
  <div class="container">
    <div class="row">
      <div v-if="!hashVal" class="col-md-12">
        <h1>待发货</h1>
        
        <b-container class="b-container" fluid>
           <b-row>
              <b-col sm="2">
                  <b-form-select v-model="selected" :options="options"></b-form-select>
              </b-col>
              <b-col sm="3">
                  <b-form-input id="input-serial" size="md" placeholder="输入部分关键字" v-model="keyword"></b-form-input>
              </b-col>
              <b-col sm="2">
                  <b-button class="btn-md btn-circle float-right" variant="success" @click="getPendingItems(keyword)">查找</b-button>
              </b-col>
              <b-col sm="2">
                  <b-button class="btn-md btn-circle" variant="warning" @click="clear()">清空</b-button>
              </b-col>
           </b-row>
        </b-container>
        
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
            <b-button class="btn-success" @click="outStock(data.item.id)">出库</b-button>
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
        <h1> {{decodeURI(this.hashVal)}} </h1>
        <b-table striped hover :items="productInfo" :fields="fields2">
        </b-table>
      </div>
    </div>
  </div>  
</template>

<script>

import common from '@/components/Common'
import axios from 'axios'

var Pending = {
  name:"Pending",
  data(){
    return {
      perPage: 7,
      currentPage: 1,
      items:[],
      fields: {
        id: {
          key: "id_number",
          label: '出库单号',
          // formatter: 'fullName',
          sortable:true,
        },
        location: {
          label: '位置',
          sortable:true
        },
        pickupTime:{
          key: "pick_time",
          label: '时间',
          sortable:true      
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
          label: '备注'
        }
      },
      // search part
      keyword:"",
      selected: 'id_number',
      options:[
        { value: 'id_number', text: '出库单号' },
        { value: 'location', text: '位置' },
      ],
    }
  },
  computed:{
    rows(){
      return this.items.length
    },
    hashVal() {
      return this.$route.hash.substring(1);
    }
  },
  methods:{
    getPendingItems(keyword){
      this.clearUp()
      var val = (keyword) ? ("&" + this.selected + "=" + keyword) :("")
      var URL = this.site + "pendingLocations?isExpire=false" + val;
      
      axios.get(URL)
        .then((res) => {
          this.items = res.data
        })
        .catch((error) => {
          console.log(error);
      });
    },
    getProductInfo(hashVal){
      // set to empty before load up
      this.clearUp()
      var URL = this.site + "pendingDetail/" + hashVal;
      axios.get(URL)
        .then((res) => {
          this.productInfo = res.data
        })
        .catch((error) => {
          console.log(error);
      });
    },
    outStock(){
      var URL = this.site + "pendingDetail/" + id;
      axios.get(URL)
        .then((res) => {
          console.log(res.data)
          var r = {"amount":[], "itemID":[]};
          for (var x of res.data){
            r.amount.push(x.amount)
            r.itemID.push(x.itemID)
          }
          // console.log(queryString)
          document.location = "in?"+queryString
        })
    },
    clear(){
      this.getPendingItems()
    },
    clearUp(){
      this.productInfo = []
      this.items = []
    }
  },
  created(){
    console.log(123)
    if (!this.hashVal){
      this.getPendingItems()
    }else{
      this.getProductInfo(this.hashVal)
    
    }
  },
  mixins: [common]
}
export default Pending
</script>
