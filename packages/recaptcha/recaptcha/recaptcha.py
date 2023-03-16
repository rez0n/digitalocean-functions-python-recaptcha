import os
import json

from urllib.parse import urlencode
from urllib.request import Request, build_opener

RECAPTCHA_REQUIRED_V3_SCORE = os.getenv('RECAPTCHA_REQUIRED_V3_SCORE', default=0.5)
RECAPTCHA_SECRET_KEY = os.getenv('RECAPTCHA_SECRET_KEY')


class RecaptchaResponse:
    def __init__(self, is_valid, error_codes=None, extra_data=None):
        self.is_valid = is_valid
        self.error_codes = error_codes or []
        self.extra_data = extra_data or {}


def recaptcha_request(params):
    request_object = Request(
        url="https://www.google.com/recaptcha/api/siteverify",
        data=params,
        headers={
            "Content-type": "application/x-www-form-urlencoded",
            "User-agent": "reCAPTCHA",
        },
    )

    # Build opener
    opener_args = []
    opener = build_opener(*opener_args)

    # Make request to reCAPTCHA API
    return opener.open(
        request_object,
        timeout=10,
    )


def recaptcha_api_request(recaptcha_response):
    params = urlencode(
        {"secret": RECAPTCHA_SECRET_KEY,
         "response": recaptcha_response,
         }
    )

    params = params.encode("utf-8")
    response = recaptcha_request(params)
    data = json.loads(response.read().decode("utf-8"))
    response.close()
    return RecaptchaResponse(
        is_valid=data.pop("success"),
        error_codes=data.pop("error-codes", None),
        extra_data=data,
    )


class RecaptchaV3Validator:
    def __init__(self, is_human, score=None, message=None, extra_data=None):
        self.is_human = is_human
        self.score = score
        self.message = message or ''
        self.extra_data = extra_data or {}


def validate_recaptcha_v3(recaptcha_response):
    response = recaptcha_api_request(recaptcha_response)

    if not response.is_valid:
        return RecaptchaV3Validator(
            is_human=False,
            message=f"reCAPTCHA validation failed due to: {response.error_codes}",
        )

    score = response.extra_data.pop('score')
    is_human = float(score) >= float(RECAPTCHA_REQUIRED_V3_SCORE)

    if is_human:
        return RecaptchaV3Validator(
            is_human=is_human,
            score=score,
            message="reCAPTCHA validation passed",
        )
    else:
        return RecaptchaV3Validator(
            is_human=is_human,
            score=score,
            message=f"reCAPTCHA validation failed due to score of {score} being lower than the required"
                    f" {RECAPTCHA_REQUIRED_V3_SCORE}"
        )
