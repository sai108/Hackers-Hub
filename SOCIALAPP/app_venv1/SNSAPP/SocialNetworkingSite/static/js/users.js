$(document).ready(function () {
    $('.send-request').click(function (event) {
        event.preventDefault();

        var friend_id = $(this).attr('id');
        var _my_id = $('#_id').val();

        $.ajax({
            url: '/friend_request/'+friend_id+'/'+_my_id,
            type: "GET",
            dataType: "json",
            contentType: "application/json",
            success: function (json) {
                $('.'+friend_id).replaceWith('<input type="submit" value="REQUEST SENT" name="{{ user.id }}" id="" data-id="{{ user.id }}" class="btn btn-larg send-request disabled {{ user.id }}" />');
            },
            error: function (data) {
                alert("Error posting" + eval(error));
            }
        });
        return false;
    });
});