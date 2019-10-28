
$(function () {

    var csrf_token = "{{ csrf_token() }}";
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrf_token);
            }
        }
    });

    var result = document.getElementById("result").innerText;
    //alert(result);
    
    if (result != "" && result != undefined && result!="none") {
        alert(result);
        result = "";
        //document.getElementById("result").innerHTML = " ";
    }
    document.getElementById("result").hidden = true;

    $('#Register').on('click', function (event) {
        window.location.href = '/register';
    });
});

