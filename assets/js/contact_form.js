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
    var form = $("form#update_contact");
    var options = {
        dataType: 'json',
        url: form.attr('action'),
        type: 'POST',
        success: successResponse,
        error: errorResponse,
    };

    form.submit(function() {
        $("#update_in").attr('disabled', 'disabled');
        $(".form-group").removeClass('has-error');
        $(".help-block").remove();
        $(".text-success").remove();
        $(".text-danger").remove();
        $(this).ajaxSubmit(options);
        return false;
    });

    $("#cancel_in").on("click", function() {
        form.resetForm();
    });

    function errorResponse(response, statusText, xhr, $form) {
        $('.update_error').html("<span class='text-danger'>Error.</span>");
        var errors = $.parseJSON(response.responseText);
        for (key in errors) {
            var contact = "#contact-" + key + " div";
            $(contact).addClass('has-error');
            $(contact).last().append('<div class="help-block">' + errors[key][0] + '</div>');
        }
        $("#update_in").removeAttr('disabled', 'disabled');
    }

    function successResponse(response, statusText, xhr, $form) {
        form.clearForm();
        for (el in response) {
            var input_el = "#id_" + el;
            $(input_el).val(response[el]);
        }
        $('.update_success').html("<span class='text-success'>Success.</span>");
        $("#update_in").removeAttr('disabled', 'disabled');
    }

    $(".datepicker").datepicker({
        dateFormat: "yy-mm-dd"
    });
    function readURL(input) {

        if (input.files && input.files[0]) {
            var reader = new FileReader();

            reader.onload = function (e) {
                $('#update_img').attr('src', e.target.result);
            }

            reader.readAsDataURL(input.files[0]);
        }
    }

    $("#update_file").change(function(){
        readURL(this);
    });
})