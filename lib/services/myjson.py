import json


def get_gassafe_users():
    f = open("./assets/gassafe.json")
    users = json.load(f)["Sheet1"]
    f.close()

    return users
