var homelistgen=(function(){

    function displayList(response){
        var n=JSON.parse(response);
        // Set all the data as array of objects without any nesting objects
        var s=n.map(function(res){
            if(typeof(res.data)== "object"){
              for (var k in res.data){
                 res[k]=res.data[k];}
              delete res.data;
              return res;
            }
        });
        // Creating columns data
        var w=s[s.length-1];
        var cd=[];
        console.log(w);
         for( var kd in w){
             var kdstr=kd.toString();
             if(w.hasOwnProperty(kdstr)){
                  var y=kdstr.charAt(0).toUpperCase() == kdstr.charAt(0) ? kdstr : kdstr.charAt(0).toUpperCase()+kdstr.substr(1);
             var e={"title": y,"data":kdstr};
             cd.push(e);
             }
         }
         console.log(cd);
        $("#example").DataTable({
            scrollY:'300px',
            scrollX:true,
            bDestroy:true,
            data:s,
            columns:cd
        });
    }
    function init(){
        $.ajax({
            url:'/display',
            success:function(response){
               return response;
            }
        }).then(displayList);
    }
    return{
        init:init
    };
})();

var runner=homelistgen;