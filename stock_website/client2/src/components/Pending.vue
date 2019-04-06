<template>
  <div class="container">
    <div class="row">
      <div class="col-md-12">
        <h1>待发货</h1>
        <hr><br>
        <b-table striped hover :items="items" :tbody-tr-class="rowClass" :fields="fields"></b-table>
      </div>
    </div>
  </div>  
</template>

<script>
var Pending = {
  name:"Pending",
  data(){
    return {
      items:[],
      fields: {
        id: {
          label: '出库单号',
          sortable:true,
        },
        productType: {
          label: '位置',
          sortable:true
        },
      },
    }
  },
  computed:{
  },
}
export default Pending
</script>
