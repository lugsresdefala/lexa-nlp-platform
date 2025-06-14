import base64
import json

class ExpiredSignatureError(Exception):
    pass

class InvalidTokenError(Exception):
    pass


def encode(payload, key, algorithm="HS256"):
    del key, algorithm
    data = json.dumps(payload).encode("utf-8")
    return base64.urlsafe_b64encode(data).decode("utf-8")


def decode(token, key, algorithms=None):
    del key, algorithms
    try:
        data = base64.urlsafe_b64decode(token.encode("utf-8"))
        return json.loads(data.decode("utf-8"))
    except Exception as exc:
        raise InvalidTokenError from exc
