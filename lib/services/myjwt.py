import jwt

SECRET = "jwtsecret"


def encode(json):
    return jwt.encode(json, SECRET, algorithm="HS256")


def decode(token):
    return jwt.decode(token, SECRET, algorithms=["HS256"])
