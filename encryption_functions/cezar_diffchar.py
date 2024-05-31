def settings(self):
    return ((("LineEdit", "Введите пароль"), ("CheckBox", "Использовать методы удлинения пароля"),),
            "Это - тестовый алгоритм шифрования.")


def check_data(self, data):
    if len(data[0]) > 0:
        return (True, "ОК")
    else:
        return (False, "Введите пароль")


def encryption_function(self, file, data):
    password = data[0]
    if len(password) == 1:
        password *= 3
    if len(password) == 2:
        password *= 2
    if data[1]:
        if len(password) % 3 == 0:
            password += "7"
    password = [i for i in password.encode("utf-8")]
    r = []
    for i in file:
        r.append((i + password[-1]) % 256)
        password = [password[-1]] + password[:-1]
    return r


def decryption_function(self, file, data):
    password = data[0]
    if len(password) == 1:
        password *= 3
    if len(password) == 2:
        password *= 2
    if data[1]:
        if len(password) % 3 == 0:
            password += "7"
    password = [i for i in password.encode("utf-8")]
    r = []
    for i in file:
        r.append((i - password[-1]) % 256)
        password = [password[-1]] + password[:-1]
    return r
