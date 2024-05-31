def settings(self):
    return ((("LineEdit", "Введите пароль"), ("CheckBox", "Кнопка"), ("Label", "А тут просто текст..."),
             ("ChoiceFile", "Выбор файла")), "Это - тестовый алгоритм шифрования.")


def check_data(self, data):
    print("отправка данных на проверку...")
    print("данные:", data)
    if len(data[0]) > 2:
        return (True, "Пароль подходит")
    else:
        return (False, "Просто вот нельзя😒")


def encryption_function(self, *args):
    return []


def decryption_function(self, *args):
    return []
