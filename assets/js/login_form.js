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
    var form = $("form#sign_in");
    var options = {
        success: successResponse,
        error: errorResponse,
        dataType: 'json',
        url: form.attr('action'),
        type: form.attr('method'),
        resetForm: true,
        clearForm: true
    };

    form.submit(function() {
        $("#sub_sign_in").attr('disabled', 'disabled');
        $(".form-group").removeClass('has-error');
        $(".help-block").remove();
        $(this).ajaxSubmit(options);
        return false;
    });

    function errorResponse(response, statusText, xhr, $form) {
        var errors = $.parseJSON(response.responseText);
        for (key in errors) {
            var group = "#group-" + key;
            $(group).addClass('has-error');
            $(group).append('<div class="help-block">' + errors[key][0] + '</div>');
        }
        $("#sub_sign_in").removeAttr('disabled', 'disabled');
    }

    function successResponse(response, statusText, xhr, $form) {
        window.location.href = response.url;
        $("#sub_sign_in").removeAttr('disabled', 'disabled');
    }
});