$(document).ready(function() {
    var title = document.title,
        staged_count = 0,
        hidden, 
        visibilityChange,
        income_count; 
        
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
            staged_count = $('.req_id').html();
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
            success: function(response) {
                if (income_count != response[0].pk) {
                    $('tbody').empty();
                    $.each(response, function(i, item) {
                        var tr = "<tr>";
                        tr +=       "<td class='req_id'>" + item.pk + "</td>";
                        tr +=       "<td>" + item.fields.method + "</td>";
                        tr +=       "<td>" + item.fields.path + "</td>";
                        tr +=       "<td>" + item.fields.status_code + "</td>";
                        tr +=       "<td>" + item.fields.remote_addr + "</td>";
                        tr +=       "<td>" + item.fields.time + "</td>";
                        tr +=       "<td>" + item.fields.priority + "</td>";
                        tr +=    "</tr>";
                        $('tbody').append(tr);
                    });
                }
                income_count = $('.req_id').html();
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