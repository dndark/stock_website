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
                var dateObj = new Date(Number(t));
                var month = dateObj.getUTCMonth() + 1; //months from 1-12
                var day = dateObj.getUTCDate();
                var year = dateObj.getUTCFullYear();
                

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
            }//end if html5 filelist support
            // else if(ActiveXObject && filePath) { //fallback to IE 6-8 support via ActiveX
            //     try {
            //         reader = new ActiveXObject("Scripting.FileSystemObject");
            //         var file = reader.OpenTextFile(filePath, 1); //ActiveX File Object
            //         output = file.ReadAll(); //text contents of file
            //         file.Close(); //close file "input stream"
            //         displayContents(output);
            //     } catch (e) {
            //         if (e.number == -2146827859) {
            //             alert('Unable to access local files due to browser security settings. ' +
            //               'To overcome this, go to Tools->Internet Options->Security->Custom Level. ' +
            //               'Find the setting for "Initialize and script ActiveX controls not marked as safe" and change it to "Enable" or "Prompt"');
            //         }
            //     }
            //   }
            //   else { //this is where you could fallback to Java Applet, Flash or similar
            //       return false;
            //   }
            // this.$refs.pathClear.value =''
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
        }
    },
}
</script>
