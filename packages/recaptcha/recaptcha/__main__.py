from recaptcha import validate_recaptcha_v3
from http import HTTPStatus


def main(args):
    recaptcha_response = args.get("recaptcha")
    if not recaptcha_response:
        return {"body": "pong"}

    recaptcha_result = validate_recaptcha_v3(recaptcha_response)

    if recaptcha_result.is_human:
        body = {
            "success": recaptcha_result.is_human,
            "score": recaptcha_result.score,
            "message": recaptcha_result.message,
        }
        return {"body": body}

    else:
        body = {
            "success": recaptcha_result.is_human,
            "score": recaptcha_result.score,
            "message": recaptcha_result.message,
        }
        return {
            "statusCode": HTTPStatus.BAD_REQUEST,
            "body": body,
        }
