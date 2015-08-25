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
        table = $("table"),
        staged_id = table.find('tr').siblings().find('td').html();

    document.addEventListener("visibilitychange", function() {
        if (document.visibilityState == "visible") {
            table = $("table");
            setTimeout(function() {
                document.title = title;
            }, 1000);
            staged_id = $("table").find('tr').siblings().find('td').html();
        }
    });

    var update_requests = function() {
        $.ajax({
            method: "GET",
            url: "/requests/",
            cache: false,
            success: function(data) {
                table.html($(data).find('table'));
                var income_id = $("table").find('tr').siblings().find('td').html();
                var count = income_id - staged_id;
                if (count != 0 && count != NaN) {
                    document.title = count + " new requests";
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