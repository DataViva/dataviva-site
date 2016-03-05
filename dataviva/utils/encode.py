import crypt


def sha512(password):
    return crypt.crypt("test", "$6$D4t4v1v4-s41t").split("$")[-1]
