var blockdata = (function (){

    function initialize(){
        $.ajax({
            url:'/display',
            success:function(response){
                return response;
            }
        }).then(handlelist);
    }

    function handlelist(res){
        var s=document.getElementById("sb").innerHTML;
        var c=Handlebars.compile(s);
        var q=JSON.parse(res);
        var html=c({datum:q});
        document.getElementById("main").innerHTML=html;
    }
    function mineData(jsonobject){
    $.ajax({
        url:"/mine",
        type:"POST",
        ContentType:"application/json",
        data:JSON.stringify(jsonobject),
        success:function(res){
            alert(res);
            
        }
    }).then(function(){
        location.reload();
    });
    }
    return{
        init:initialize,
        mine:mineData
    };
})();

var d=blockdata;
function displayminedata(p){
    event.preventDefault();
    var myform=$("#"+p);
    var readonly = myform.find(':input[readonly]').removeAttr('readonly');
      var dataset = myform.serializeArray();
        readonly.attr('readonly','readonly');
        var dr={},da={};
        dataset.map(function(dat){
            if(dat.name=='index' || dat.name=='hash' || dat.name=='prevhash' || dat.name=='nonce' || dat.name=='timestamp')
            dr[dat.name]=dat.value;
            else
            da[dat.name]=dat.value;
          });
          dr.data=da;
          console.log(dr);
        d.mine(dr);
}