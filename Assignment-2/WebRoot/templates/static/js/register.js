
$(function () {

    var result = document.getElementById("success").innerHTML;
    //alert(result);
 
    if (result != "" && result != undefined && result!="none") {
        alert(result);
        result = "";
        //document.getElementById("result").innerHTML = " ";
    }
    document.getElementById("success").hidden = true;

    $('#Register').on('click', function (event) {
        window.location.href = '/register';
    });
});

