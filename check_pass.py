import re  # импорт регулярных выражений для шустрой проверки


def password_check(password):  # функция проверки пароля
    length_error = len(password) < 8  # проверка на длину
    print(length_error)
    # проверка на наличие цифр
    digit_error = re.search(r"\d", password) is None
    # проверка на наличие букв верхнего регистра
    uppercase_error = re.search(r"[A-Z]", password) is None
    # проверка на наличие букв нижнего регистра
    lowercase_error = re.search(r"[a-z]", password) is None
    symbol_error = re.search(  # проверка на наличие символов
        r"[ !@#$%&'()*+,-./[\\\]^_`{|}~"+r'"]', password) is None
    res = {  # общий сбор
        'Пароль короче 8 символов': length_error,
        'Пароль не содержит цифр': digit_error,
        'Пароль не содержит букв верхнего регистра': uppercase_error,
        'Пароль не содержит букв нижнего регистра': lowercase_error,
        'Пароль не содержит специальных символов': symbol_error,
    }
    return res  # возвращаем выводы проверок
