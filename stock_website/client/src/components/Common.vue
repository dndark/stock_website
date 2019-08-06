<script>

import axios from 'axios'
export default {

    name:"Common",
    data(){
        return{
            // site: 'http://localhost:5000/',
            site:"/api/",
            
            dismissSecs: 3,
            dismissCountDown: 0,
            nameOptions:["所有人","张淑芳","刘伟","李彩霞","韩晓波","任艳红","王婷婷","张艳梅","贾紫娟","常芳萍","李艳茹","徐佳毅","李国栋","张银芳","张海燕","春桥科技"],
            fileInit:{
                
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
                stockNumber: {
                    label: '库存总数',
                    sortable:true
                },
            }
        }
    },
    methods:{
        dateFormat(t){
            // var dateNum =  Date.parse(t);
            if (t){
                var dateObj = new Date(t);
                var month = dateObj.getUTCMonth() + 1; //months from 1-12
                var day = dateObj.getUTCDate();
                var year = dateObj.getUTCFullYear();
                console.log(dateObj)
                return  year + "/" + month + "/" + day;
            }
            return ''
        },
        occurrences(arr){
            var counts = {}
            for (var i = 0; i < arr.length; i++) {
                var num = arr[i];
                counts[num] = counts[num] ? counts[num] + 1 : 1;
            }
            return counts
        },

        readFile(e){
            // e.preventDefault()
            // IN CASE TO USE THIS FUNCTION, YOU NEED TO DEFINED THE LOADINFO IN YOUR VUE COMPONENT
            
            var self = this
            var filePath = e.target
            console.log(filePath)
            var reader = new FileReader();
            var output = ""; //placeholder for text output
            // only support txt file for now
            if(filePath.files && filePath.files[0] && filePath.files[0].name.split('.').pop() == "txt") {
                reader.onload = function (e) {
                    // parse the txt file, split by new line
                    output = String(e.target.result);
                    var outputArray = output.split("\n");
                    // remove enter key
                    for (var i=0; i < outputArray.length; i++){
                        outputArray[i] = outputArray[i].replace(/\r/g, '')
                    }
                    // remove empty value
                    outputArray = outputArray.filter(function(el) { return el; });
                    // console.log(outputArray)
                    var arr = self.occurrences(outputArray)
                    for (var x in arr){
                        self.loadInfo(x, arr[x])
                    }

                };//end onload()
                reader.readAsText(filePath.files[0]);
            }
            return true;
        },
        // TODO YOU MUST IMPLYMENT THE LOADINFO IN YOUR LOCAL SCOPE
        // loadInfo(itemID, arr){
        //     // console.log(itemID, arr)
        //     return 
        // },
        removeSpecialChar(s){
          var pattern = /[a-zA-Z0-9_]{1}/;
          var rs = ""; 
          if (s == undefined){
            s = ''
          }
          for (var i = 0; i < s.length; i++) { 
            var single = s.substr(i, 1);
          
            if(single.match(pattern)){
              rs = rs + single;
             } 
           }
          
          return rs;
        },
        
        updateDate(items){
            for (var i=0; i< items.length; i++ ){
                items[i].lastModifiedDate = Date.now()
            }
        },
        ObjectToQueryString(Obj){
            var queryString = Object.keys(Obj).map(key => key + '=' + Obj[key]).join('&');
            return queryString
        },
        QueryStringToObject(){    
            var url = location.search; //获取url中"?"符后的字串
            var theRequest = new Object();
            if (url.indexOf("?") != -1) {
                var str = url.substr(1);
                var strs = str.split("&");
                for(var i = 0; i < strs.length; i ++) {
                    theRequest[strs[i].split("=")[0]] = (strs[i].split("=")[1]).split(",");
                }
            }
            return theRequest;
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
}
</script>
