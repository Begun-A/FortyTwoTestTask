$(document).ready(function() {
    var getCookie = function(c_name) {
        if (document.cookie.length > 0) {
            c_start = document.cookie.indexOf(c_name + "=");
            if (c_start != -1) {
                c_start = c_start + c_name.length + 1;
                c_end = document.cookie.indexOf(";", c_start);
                if (c_end == -1) c_end = document.cookie.length;
                return unescape(document.cookie.substring(c_start,c_end));
            }
        }
        return "";
    };
    $.ajaxSetup({
        headers: {
            'X-CSRFToken': getCookie("csrftoken")
        }
    });
    var title = document.title,
        staged_count = 0,
        hidden, 
        visibilityChange; 
        
    if (typeof document.hidden !== "undefined") { // Opera 12.10 and Firefox 18 and later support 
        hidden = "hidden";
        visibilityChange = "visibilitychange";
    } else if (typeof document.mozHidden !== "undefined") {
        hidden = "mozHidden";
        visibilityChange = "mozvisibilitychange";
    } else if (typeof document.msHidden !== "undefined") {
        hidden = "msHidden";
        visibilityChange = "msvisibilitychange";
    } else if (typeof document.webkitHidden !== "undefined") {
        hidden = "webkitHidden";
        visibilityChange = "webkitvisibilitychange";
    }
    document.addEventListener(visibilityChange, function() {
        if (document.visibilityState == hidden) {
            staged_count = $('#req_id').html();
        }
        if (document.visibilityState == "visible") {
            setTimeout(function() {
                document.title = title;
            }, 1000);
            staged_count = 0;
        }
    });

    var update_requests = function() {
        $.ajax({
            method: "GET",
            url: "/requests/",
            cache: false,
            success: function(data) {
                $('tbody').replaceWith($(data).find('tbody'));
                var income_count = $('#req_id').html();
                if (staged_count != 0 && income_count > staged_count) {
                    var count_req = income_count - staged_count;
                    document.title = count_req + " new requests";
                }
            },
            error: function(response, data, xhr, errmsg, err) {
                console.log(xhr.status);
                console.log(errors);
            }          
        });
    };
    setInterval(update_requests, 1000);
});