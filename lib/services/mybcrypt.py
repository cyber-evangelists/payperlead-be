import bcrypt


def hash(string):
    return bcrypt.hashpw(string.encode(), salt=bcrypt.gensalt())


def check(string, hashed_string):
    return bcrypt.checkpw(string.encode(), hashed_string.encode())
