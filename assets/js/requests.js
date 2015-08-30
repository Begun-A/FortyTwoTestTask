$(document).ready(function() {
    var title = document.title,
        staged_count = 0,
        hidden, 
        visibilityChange; 
        
    if (typeof document.hidden !== "undefined") { 
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
                if (staged_count > 0 && income_count > staged_count) {
                    var count_req = income_count - staged_count;
                    document.title  = "(" + count_req +  ") " + title;
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