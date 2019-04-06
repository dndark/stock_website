<template>
  <div class="container">
    <div class="row">
      <div class="col-md-12">
        <h1>统计</h1>
        <hr><br>
        <b-table class="table table-hover"
          id = "myTable"
          :items="ModifiedOverViewItem"
          :per-page="perPage"
          :current-page="currentPage"
          :fields="fields">
        </b-table>
          <div class="overflow-auto">
              <b-pagination
                align="fill"
                v-model="currentPage"
                :total-rows="rows"
                :per-page="perPage"
                aria-controls="myTable"
              />
            </div>
      </div>
      
    </div>
   
  </div>
</template>

<script>

import common from '@/components/Common'
import axios from 'axios'

export default {
    name:"Overview",
    data() {
      return {
        perPage: 8,
        currentPage: 1,
        OverviewItems:[],

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
              label: '库存',
              sortable:true
            },
            lastModifiedDate:{
              label: '修改时间',
              sortable:true
            },
            info:{
              label: '备注',
            },
            location: {
              label: '位置',
              sortable:true
            },
        },
      }
    },
    computed: {
      rows() {
        return this.OverviewItems.length
      },
      ModifiedOverViewItem(){
        var result = []
        for (var value of this.OverviewItems){
          // var newItem = {}
          
          // newItem["条纹码"] = value["id"]
          // newItem["公司"] = value["company"]
          // newItem["型号"] = value["modelNumber"]
          
          // newItem["种类"] = value["productType"]
          // newItem["库存总数"] = value["stockNumber"]
          // newItem["位置"] = value["location"]
          value.lastModifiedDate = this.dateFormat(value["lastModifiedDate"])
          
          // newItem["备注"] = value["info"]
          // result.push(newItem)
        }
        return this.OverviewItems
      }
    },
    methods:{
        getAllStocks(){
            const path = this.site+"stocks"
            axios.get(path)
                .then((res) => {
                    this.OverviewItems = res.data.items;
                })
                .catch((error) => {
                // eslint-disable-next-line
                console.error(error);
                });
        }
    },
    
    created(){
        this.getAllStocks()
    },
    mixins: [common]
}
</script>
