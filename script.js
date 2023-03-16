$(document).ready(function () {

    const apiUrl = 'https://faas-fra1-afec6ce7.doserverless.co/api/v1/web/fn-04503e26-6c2d-4463-8e0f-d7408616883f/recaptcha/recaptcha'
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