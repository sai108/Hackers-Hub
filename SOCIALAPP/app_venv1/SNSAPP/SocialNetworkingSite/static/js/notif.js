$(document).ready(function () {
    $('.accept-request').click(function (event) {
        event.preventDefault();

        var friend_id = $(this).attr('id');
        var _my_id = $('#_id').val();

        $.ajax({
            url: '/accept_request/'+friend_id+'/'+_my_id,
            type: "GET",
            dataType: "json",
            contentType: "application/json",
            success: function (json) {
                $('.'+friend_id).replaceWith('<input type="button" value="Accepted Request" name="" id="" data-id="" class="btn btn-larg send-request disabled {{ user.id }}" />');
            },
            error: function (data) {
                alert("Error posting" + eval(error));
            }
        });
        return false;
    });
});

