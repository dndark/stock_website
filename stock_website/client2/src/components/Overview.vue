<template>
  <div class="container">
    <div class="row">
      <div class="col-md-12">
        <h1>统计</h1>
        <hr>
        <b-container class="b-container" fluid>
           <b-row>
              <b-col sm="2">
                  <b-form-select v-model="selected" :options="options"></b-form-select>
              </b-col>
              <b-col sm="3">
                  <b-form-input id="input-serial" size="md" placeholder="输入部分关键字" v-model="keyword"></b-form-input>
              </b-col>
              <b-col sm="2">
                  <b-button class="btn-md btn-circle float-right" variant="success" @click="getKeywordInfo()">查找</b-button>
              </b-col>
              <b-col sm="2">
                  <b-button class="btn-md btn-circle" variant="warning" @click="clear()">清空</b-button>
              </b-col>
           </b-row>
        </b-container>
        <br>
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
        // search part
        options:[
          { value: 'id', text: '条纹码' },
          { value: 'productType', text: '种类' },
          { value: 'company', text: '厂家' },
          { value: 'modelNumber', text: '型号' },
          { value: 'stockNumber', text: '库存' },
          { value: 'location', text:'位置'}
        ],
        selected:'id',

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

        keyword:"",
      }
    },
    computed: {
      rows() {
        return this.OverviewItems.length
      },
      ModifiedOverViewItem(){
        var result = []
        for (var value of this.OverviewItems){
          value.lastModifiedDate = this.dateFormat(value["lastModifiedDate"])
        }
        return this.OverviewItems
      }
    },
    methods:{
        getAllStocks(){
          var path = this.site + "stocks";
          this.getOverviewItems(path)
        },
        getKeywordInfo(){
          var path = this.site + "stocks/type/" + this.selected + "/" + this.keyword ;
          this.getOverviewItems(path)
        },
        getOverviewItems(path){
          axios.get(path)
            .then((res) => {
                this.OverviewItems = res.data.items;
            })
            .catch((error) => {
            // eslint-disable-next-line
              console.error(error);
            });
          return 
        },
        clear(){
          this.keyword = ''
          this.selected = 'id'
          this.getAllStocks()
          return
        }
    },
    
    created(){
        this.getAllStocks()
    },
    mixins: [common]
}
</script>
