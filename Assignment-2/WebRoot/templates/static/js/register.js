window.onload=function(){
    //var resultsss = {{result}};
    //alert("hi"+resultsss);
    var result = document.getElementById("result").innerHTML;

    //alert("2"+result);
    if(result!="" && result!=undefined){
        alert(result);
        result =""; 
        document.getElementById("result").value=" " ;
    }
    document.getElementById("result").hidden=true;
    
};