from flask import request
import base64  # библиотека для работы с битами картинок


def work_image():  # функция обработки изображений из форм
    image = request.files['file']  # достём изображение из формы
    bytestring = image.read()  # читаем биты изображения
    if bytestring:  # если картинка есть
        image = base64.b64encode(bytestring).decode(
            'utf-8')  # преобразуем в удобный нам формат
    else:  # елси нет, достаём свою
        with open('static/img/emptiness.jpg', 'rb') as file:
            bytestring = file.read()
            image = base64.b64encode(bytestring).decode('utf-8')
    return image  # возвращаем нужную нам картинку
