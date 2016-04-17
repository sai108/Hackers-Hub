$(document).ready(function(){
    $('#chat-form').on('submit', function (event) {
        event.preventDefault();

        var friend_id = $('#friend_id').val();
        var my_id = $('#_id').val();

        $.ajax({
            url: '/post_chat/'+my_id+'/'+friend_id,
            type: "POST",
            data: JSON.stringify({
                msg_box: $('#chat-msg').val()
            }),
            dataType: "json",
            contentType: "application/json",

            success: function (json) {
                $('#chat-msg').val('');
                $('#msg-list').append('<li class="text-right list-group-item" id ="{{ obj.id }}" style="color: #6a1b9a" >' + json.msg + ' <a href="/delete_msg/{{ id }}/{{ obj.friends_id }}/{{ obj.id }}" class="delete-request" id="{{ obj.id }}" data-id="{{ obj.id }}"> <span  class="glyphicon glyphicon-trash"></span> </a></li>');
                var chatList = document.getElementById('msg-list-div');
                chatList.scrollTop = chatList.scrollHeight;
            },
            error: function (data) {
                alert("Error posting" + eval(error));
            }
        });
        return false;
    });
});


$(document).ready(function(){
          $('.delete-request').click(function (event) {
              event.preventDefault();

              var msg_id = $(this).attr('id');
              var friend_id = $('#friend_id').val();
              var _my_id = $('#_id').val();

              $.ajax({
                  url: '/delete_msg/'+ _my_id + '/' +friend_id + '/'+ msg_id,
                  type: "GET",
                  dataType: "json",
                  contentType: "application/json",
                  success: function (json) {
                      getMessages();
                      $('#'+msg_id).replaceWith('<input hidden/>');
                  },
                  error: function (data) {
                      alert("Error posting" + eval(error));
                  }
              });
              return false;
          });
});



function getMessages() {
    if (!scrolling) {
        var friend_id = $('#friend_id').val();
        var my_id = $('#_id').val();

        $.get('/message/'+ my_id+'/'+ friend_id, function (messages) {
            $('#msg-list').html(messages);
                var chatList = document.getElementById('msg-list-div');
                chatList.scrollTop = chatList.scrollHeight;
            });
        }
        scrolling = false;
}


var scrolling = false;
$(function () {
    $('#msg-list-div').on('scroll', function () {
        scrolling = true;
    });
    refreshTimer = setInterval(getMessages, 2500);
});


$(document).ready(function () {
    $('#send').attr('disabled', 'disabled');
       $('#chat-msg').keyup(function () {
            if ($(this).val() != '') {
                $('#send').removeAttr('disabled');
            }
            else {
                $('#send').attr('disabled', 'disabled');
            }
       });
});




// using jQuery
//function getCookie(name) {
//    var cookieValue = null;
//    if (document.cookie && document.cookie != '') {
//        var cookies = document.cookie.split(';');
//        for (var i = 0; i < cookies.length; i++) {
//            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
//            if (cookie.substring(0, name.length + 1) == (name + '=')) {
//                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//                break;
//            }
//        }
//    }
//    return cookieValue;
//}

//var csrftoken = getCookie('csrftoken');

//function csrfSafeMethod(method) {
            // these HTTP methods do not require CSRF protection
//    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
//}


//$.ajaxSetup({
//    beforeSend: function (xhr, settings) {
//        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
//            xhr.setRequestHeader("X-CSRFToken", csrftoken);
//        }
//    }
//});