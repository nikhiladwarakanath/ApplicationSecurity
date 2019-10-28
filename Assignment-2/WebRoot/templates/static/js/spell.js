$(function () {

    var csrf_token = "{{ csrf_token() }}";
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrf_token);
            }
        }
    });

    $("#logout").on('click', function () {
        var tmp = "inside";
        //alert(tmp);
        $.ajax({
            url: '/logout',
            type: 'GET',
            contentType: false,
            processData: false,
            success: function (data) {
                // alert(data);
                // console.log(data);
                window.location.href = data;
            }
        });
        return false;
    });
});