$("#myForm").submit(function (event) {

    var formData = new FormData(this);
    //formData.append("uploadFiles", $('[name="file"]')[0].files[0]);
    event.stopPropagation();
    event.preventDefault();
    $.ajax({
        url: '/spellcheck',
        data: formData,
        processData: false,
        contentType: false,
        type: 'POST',
        success: function (data) {
            display_txt = data.replace(/\n/g, "<br />");
            var newtag = "<p id='misspelled'>Misspelled Words are: <br/> " + display_txt + " </p>";
            $("body").append(newtag);
            //alert(data);
            //loadFiles()
        }
    });
    return false;
});
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