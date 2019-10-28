

    
$(function () {
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