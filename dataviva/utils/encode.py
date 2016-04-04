import crypt


def sha512(val):
    return crypt.crypt(val, "$6$D4t4v1v4-s41t").split("$")[-1]
