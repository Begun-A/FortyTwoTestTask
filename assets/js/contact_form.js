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
    var form_img = $("#update_img_link").attr("href");
    var options = {
        dataType: 'json',
        url: form.attr('action'),
        type: 'POST',
        success: successResponse,
        error: errorResponse,
    };
    function error_remove() {
        $(".form-group").removeClass('has-error');
        $(".help-block").remove();
        $(".text-success").remove();
        $(".text-danger").remove();
    }
    form.submit(function() {
        error_remove();
        $("#update_in").attr('disabled', 'disabled');
        $(this).ajaxSubmit(options);
        return false;
    });

    $("#cancel_in").on("click", function() {
        form.resetForm();
        error_remove();
        $("#update_img").attr("src", form_img);
    });

    function errorResponse(response, statusText, xhr, $form) {
        $('.update_error').html("<span class='text-danger'>Error.</span>");
        $("#update_in").removeAttr('disabled', 'disabled');
        var errors = $.parseJSON(response.responseText);
        for (key in errors) {
            var contact = "#contact-" + key + " div";
            $(contact).addClass('has-error');
            $(contact).last().append('<div class="help-block">' + errors[key][0] + '</div>');
        }
    }

    function successResponse(response, statusText, xhr, $form) {
        form.clearForm();
        for (el in response) {
            if (el == "photo") {
                continue;
            }
            var input_el = "#id_" + el;
            $(input_el).val(response[el]);
        }
        $("#update_img").attr("src", MEDIA_URL + response.photo);
        $("#update_img_link").attr("href", MEDIA_URL + response.photo);
        $("#update_img_link").html(MEDIA_URL + response.photo);
        $('.update_success').html("<span class='text-success'>Changes have been save</span>");
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

    $("#id_photo").change(function(){
        readURL(this);
    });
})