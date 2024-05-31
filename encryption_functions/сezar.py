def settings(self):
    return ((("LineEdit", "Введите пин-код"),),
            '  Алгоритм шифрования "cezar" - это алгоритм созданый по мотивам алгоритма цезаря. \n\n  Принцып работы:\nАлгоритм представляет файл как список чисел от 0 до 255(каждое число - значение байта). Затем к каждому элементу этого списка он прибавляет число(заданное как пин-код), а затем от получившивося числа он берёт остаток от деления на 256, потом он весь этот список чисел преоброзовывает в список байт и записывает в файл. Готово.\n\n  Примечание: Файл зашифрованный этим алгоритмом очен легко взломать(достаточно перебрать 256 возможных вариантов)')


def check_data(self, data):
    try:
        pin = int(data[0])
    except BaseException:
        return (False, "пин-код!")
    if pin != 0:
        return (True, "Хорошо!")
    else:
        return (False, "Данный пин-код не подходит!")


def encryption_function(self, file, data):
    password = int(data[0])
    r = [(i + password) % 256 for i in file]
    return r


def decryption_function(self, file, data):
    password = int(data[0])
    r = [(i - password) % 256 for i in file]
    return r
