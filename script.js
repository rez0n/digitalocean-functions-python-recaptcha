$(document).ready(function () {

    const apiUrl = 'https://recaptcha-functions-demo-zeeyh.ondigitalocean.app/functions/recaptcha/recaptcha'
    const reCaptchaKey = '6LeYKQUlAAAAAIkK4cvk5Q5loTO-z_MKenVoqHIG'

    let notyf = new Notyf({
        duration: 5000,
    });

    $('#subscribe-form').submit(function (e) {

        e.preventDefault();
        let form = $(this);

        grecaptcha.ready(function () {
            grecaptcha.execute(reCaptchaKey, {action: 'submit'}).then(function (token) {
                $.ajax({
                    url: apiUrl,
                    type: 'post',
                    dataType: 'json',
                    data: form.serialize() + "&recaptcha=" + token,
                    success: function (response) {
                        notyf.success(response.message);
                        $('#alert').html(response.message)
                        $('#alert').removeClass('d-none')
                        form.trigger("reset");
                    },
                    error: function (response) {
                        let message;
                        if (response.responseJSON) {
                            message = response.responseJSON.message;
                        } else {
                            message = 'Unknown error occurred';
                        }
                        notyf.error(message);
                    }
                });
            });
        });

    });

});