<script>

import axios from 'axios'
export default {

    name:"UnpayCommon",
    data(){
        return{
            site:"/api/",
            yearOptions: [2019, 2018 ],
            yearSelected: 2019,
            // nameOptions:["所有人","张淑芳","刘伟","李彩霞","韩晓波","任艳红","王婷婷","张艳梅","贾紫娟","常芳萍","李艳茹","徐佳毅","李国栋","张银芳","张海燕","春桥科技"],
            nameOptions:[
                {value:"张淑芳",text:"张淑芳"},
                {value:"刘伟",text:"刘伟"},
                {value:"李彩霞",text:"李彩霞"},
                {value:"韩晓波",text:"韩晓波"},
                {value:"王婷婷",text:"王婷婷"},
                {value:"张艳梅",text:"张艳梅"},
                {value:"贾紫娟",text:"贾紫娟"},
                {value:"常芳萍",text:"常芳萍"},
                {value:"徐佳毅",text:"徐佳毅"},
                {value:"李国栋",text:"李国栋"},
                {value:"张银芳",text:"张银芳"},
                {value:"张海燕",text:"张海燕"},
                {value:"春桥科技",text:"春桥科技"},
            ],

            nameSelected:"所有人",
            perPage: 15,
            currentPage: 1,
            items:[],
            // this is copy of items but only render at created
            onceItems:[],
            itemCount:[]
        }
    },
    computed:{
        rows(){
            return this.items.length
        },
        // getItems(){
        //     var url = this.getUrl
        //     var self = this
        //     var a = self.nameSelected
        //     axios.get(url)
        //         .then((res) => {
        //         this.items = res.data
        //         self.currentPage = 1
        //         // onceItem need to be corresponding to the correct year, so if nameSelected 
        //         // is all, we could just copy the res.data obj to onceItems. if the nameSelected
        //         // is not the all, we need to make one more extract API call, to fetch all user information
        //         // this may cause redundant call
        //         if (self.nameSelected == "所有人"){
        //             self.onceItems = JSON.parse(JSON.stringify(res.data));
        //         }else{
        //             url = url.replace(self.nameSelected,"所有人")
        //             axios.get(url).then((res)=>{self.onceItems = JSON.parse(JSON.stringify(res.data));})
        //         }
                
        //         })
        //         .catch((error) => {
        //         console.log(error);
        //     });
        // },
        nameOptions2(){
            var newList = [{value:"所有人", text:"所有人("+this.onceItems.length+")"}]
            for (var x of this.nameOptions){
                if (x.name != "所有人"){
                    var countNumberOfName = this.onceItems.filter(item => item.sc_sponsor === x.value).length;
                    newList.push({value:x.value, text:x.text+"("+countNumberOfName+")"})
                }
            }
            return newList
        }
    },
    methods:{
        getItems(){
            console.log(123)
            // var url = this.site + "unPayItems?";
            // url += 'year='+this.yearSelected+"&" + 'name='+this.nameSelected
            var url = this.url
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
        postUpdateItem(value){
            var url = this.site + "updateUnPayItem";
            var self = this
            axios.post(url,{
                handle_score: 10,        
                sc_code: value.sc_code  
            })
            .then((res) => {
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
        dateFormat(t){
            if (t){
                var dateObj = new Date(t);
                var month = dateObj.getUTCMonth() + 1; //months from 1-12
                var day = dateObj.getUTCDate();
                var year = dateObj.getUTCFullYear();
                return  year + "/" + month + '/'+ day;
            }
            return ''
        },
        toString(value) {
            if (!value) { return ''
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
                // console.log(a[key])
                // return Number(a[key]) < Number(b[key]) ? -1 : Number(a[key]) > Number(b[key]) ? 1 : 0
            } else{
                return this.toString(a[key]).localeCompare(this.toString(b[key]), undefined, {
                numeric: true
                })
            }
        },
        numFormat(value){
            let realVal = parseFloat(value).toFixed(0)
            return realVal
        },
        precentFormat(value){
            let realVal = parseFloat(value).toFixed(2) +"%"
            return realVal
        },
    },
    created(){
        this.getItems()
    },
}
</script>
