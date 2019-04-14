function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$(document).ready(function () {
    $(".like").click(function (event) {
        var btn = $(this);
        var prefix = "/questions"
        if(btn.hasClass("answ_button")) prefix = "/answer"
        var id = $(this).attr('id').split('like')[1];
        if((btn.children('i').css('color') =='rgb(33, 37, 41)') && ($("#dislike" + id).children('i').css('color') =='rgb(33, 37, 41)')) {
            $.ajax({
                type: "POST",
                url: prefix+"/edit_rate/" + id + "/",
                data: {
                    csrfmiddlewaretoken: getCookie("csrftoken"),
                    'isLike': 1
                },
                success: function (resp) {
                    btn.children('i').replaceWith('<i class="fa fa-fw fa-thumbs-up" style="color:green"></i>');
                    $("#rate" + id).text(resp)
                },
                statusCode: {
                    401: function (resp) {
                        window.location.href = "{% url 'login' %}"
                    }
                }
            });
        }
        else if ((btn.children('i').css('color') =='rgb(0, 128, 0)') && ($("#dislike" + id).children('i').css('color') =='rgb(33, 37, 41)')){
            $.ajax({
                type: "POST",
                url: prefix+"/edit_rate/" + id + "/",
                data: {
                    csrfmiddlewaretoken: getCookie("csrftoken"),
                    'isLike': 2
                },
                success: function (resp) {
                    btn.children('i').replaceWith('<i class="fa fa-fw fa-thumbs-o-up" style="color:rgb(33, 37, 41)"></i>');
                    $("#rate" + id).text(resp)
                },
                statusCode: {
                    401: function (resp) {
                        window.location.href = "{% url 'login' %}"
                    }
                }
            });
        }
        if ((btn.children('i').css('color') =='rgb(33, 37, 41)') && ($("#dislike" + id).children('i').css('color') =='rgb(255, 0, 0)')){
            $.ajax({
                type: "POST",
                url: prefix+"/edit_rate/" + id + "/",
                data: {
                    csrfmiddlewaretoken: getCookie("csrftoken"),
                    'isLike': 4
                },
                success: function (resp) {
                    btn.children('i').replaceWith('<i class="fa fa-fw fa-thumbs-up" style="color:green"></i>');
                    $("#rate" + id).text(resp)
                    $("#dislike" + id).children('i').replaceWith('<i class="fa fa-fw fa-thumbs-o-down" style="color:rgb(33, 37, 41)"></i>');
                },
                statusCode: {
                    401: function (resp) {
                        window.location.href = "{% url 'login' %}"
                    }
                }
            });
        }

    });

    $(".dislike").click(function (event) {
        var btn = $(this);
        var id = $(this).attr('id').split('like')[1];
        var prefix = "/questions"
        if(btn.hasClass("answ_button")) prefix = "/answer"
        if(btn.children('i').css('color') =='rgb(33, 37, 41)' && ($("#like" + id).children('i').css('color') =='rgb(33, 37, 41)')) {
            $.ajax({
                type: "POST",
                url: prefix+"/edit_rate/" + id + "/",
                data: {
                    csrfmiddlewaretoken: getCookie("csrftoken"),
                    'isLike': 0
                },
                success: function (resp) {
                    btn.children('i').replaceWith('<i class="fa fa-fw fa-thumbs-down" style="color:red"></i>');
                    $("#rate" + id).text(resp)
                },
                statusCode: {
                    401: function (resp) {
                        window.location.href = "{% url 'login' %}"
                    }
                }


            });
            return false;
        }
        else if(btn.children('i').css('color') =='rgb(255, 0, 0)' && ($("#like" + id).children('i').css('color') =='rgb(33, 37, 41)')) {
            $.ajax({
                type: "POST",
                url: prefix+"/edit_rate/" + id + "/",
                data: {
                    csrfmiddlewaretoken: getCookie("csrftoken"),
                    'isLike': 3
                },
                success: function (resp) {
                    btn.children('i').replaceWith('<i class="fa fa-fw fa-thumbs-o-down" style="color:rgb(33, 37, 41)"></i>');
                    $("#rate" + id).text(resp)
                },
                statusCode: {
                    401: function (resp) {
                        window.location.href = "{% url 'login' %}"
                    }
                }


            });
            return false;

        }
        if ((btn.children('i').css('color') =='rgb(33, 37, 41)') && ($("#like" + id).children('i').css('color') =='rgb(0, 128, 0)')){
            $.ajax({
                type: "POST",
                url: prefix+"/edit_rate/" + id + "/",
                data: {
                    csrfmiddlewaretoken: getCookie("csrftoken"),
                    'isLike': 5
                },
                success: function (resp) {
                    btn.children('i').replaceWith('<i class="fa fa-fw fa-thumbs-down" style="color:red"></i>');
                    $("#rate" + id).text(resp)
                    $("#like" + id).children('i').replaceWith('<i class="fa fa-fw fa-thumbs-o-up" style="color:rgb(33, 37, 41)"></i>');
                },
                statusCode: {
                    401: function (resp) {
                        window.location.href = "{% url 'login' %}"
                    }
                }
            });
        }
    });


});