# Импортируем необходимые классы.
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram import ReplyKeyboardMarkup  # для бота
import datetime  # для рассылки
import requests  # для сбора данных
import pyshorteners  # для коротких ссылок

short = pyshorteners.Shortener()  # объект класса, укорачивающего ссылки


def start(update, context):  # команда старта
    update.message.reply_text(
        "Я - бот проекта News Guide.\nЧтобы узнать, что я могу, введите команду /help\n"
        "Сайт проекта - http://kirillka00.pythonanywhere.com/home", reply_markup=markup)


def helppy(update, context):  # команда помощи со списком и описанием команд
    update.message.reply_text(
        "/fresh_news - одна свежая новость\n\n"
        "/some_news - пять свежих новостей подряд\n"
        "Использование: /some_news <количество>(по умолчанию 5)\n\n"
        "/search - поиск новости по ключевому слову\n"
        "Использование: /search <ключевое слово>\n\n"
        "/course - актуальный курс валют\n"
        "Использование: /course <количество валюты>(по умолчанию 1)\n\n"
        "/notif_news - включить/изменить ежедневную рассылку новостей и курса валют в определённое время\n"
        "Использование: /notif_news <время>\n"
        "Время в формате 00:00\n\n"
        "/off_notif_news - отключить ежедневную рассылку\n\n"
        "/site - ссылка на сайт проекта News Guide\n\n"
        "/contacts - контакты разработчика\n\n"
        "/help - список команд. вы только что вызвали.")


# команда которая отправляет пользователю свежайшую (для апишки) новость на русском языке
def fresh_news(update, context):
    # собираем запрос
    request = "https://newsapi.org/v2/top-headlines?country=ru&apiKey=499c7a59bd714f83abbee6644022628e"
    response = requests.get(request)  # Выполняем запрос.
    news_api = []  # список для хранения будущих новостей
    if response:
        json_response = response.json()  # преобразуем ответ в json-объект
        responce = json_response['articles']  # достаём новости
        for article in responce:  # пробегаемся по ним, оставляя только нужное
            source = (article['source']['name'])
            title = (article['title'])
            url = article['url']
            news_api.append({'source': source, 'title': title, 'url': url})  # добавляем всё, что нужно, в список
        # отправляем пользователю заголовок, источник и ссылку на новость
        update.message.reply_text(f'{news_api[0]["title"]}\n'
                                  f'Источник - {news_api[0]["source"]}\n'
                                  f'Читать новость - {short.tinyurl.short(news_api[0]["url"])}')
    else:  # если что-то пошло не так, выводим в консоль ошибку
        update.message.reply_text('Техническая ошибка. Повторите попытку позже.')  # сообщаем об ошибке пользователю
        print('Ошибка:')
        print(request)
        print("Http статус:", response.status_code, "(", response.reason, ")")


def some_news(update, context):  # команда выводящая несколько новостей
    # собираем запрос
    request = "https://newsapi.org/v2/top-headlines?country=ru&apiKey=499c7a59bd714f83abbee6644022628e"
    response = requests.get(request)  # Выполняем запрос.
    news_api = []  # список для хранения будущих новостей
    if response:
        json_response = response.json()  # Преобразуем ответ в json-объект
        responce = json_response['articles']  # достаём новости
        for article in responce:  # пробегаемся по ним, собирая всё "по полочкам"
            source = (article['source']['name'])
            title = (article['title'])
            url = article['url']
            time = article['publishedAt']
            # добавляем всё, что нужно, в список
            news_api.append({'source': source, 'title': title, 'url': url, 'time': time})
        k = 5  # количество новостей по умолчанию
        if context.args and context.args[0].isdigit():  # если аргумент (количество новостей) был передан
            if 1 < int(context.args[0]) <= len(news_api): # в лучшем случае
                k = int(context.args[0])
                for i in range(k):
                    update.message.reply_text(f'{news_api[i]["title"]}\n'
                                              f'Источник - {news_api[i]["source"]}\n'
                                              f'Опубликовано {news_api[i]["time"][:10]} '
                                              f'в {news_api[i]["time"][11:16]}\n'
                                              f'Читать новость - {short.tinyurl.short(news_api[i]["url"])}')
            elif int(context.args[0]) == 1:  # в плохих случаях
                update.message.reply_text('Воспользуйтесь командой /fresh_news')
            elif int(context.args[0]) > len(news_api):
                update.message.reply_text(f'Превышен предел. Максимальное количество новостей за раз - {len(news_api)}')
            else:
                update.message.reply_text('Невозможно выполнить ваш запрос')
        else:
            for i in range(k):
                update.message.reply_text(f'{news_api[i]["title"]}\n'
                                          f'Источник - {news_api[i]["source"]}\n'
                                          f'Опубликовано {news_api[i]["time"][:10]} '
                                          f'в {news_api[i]["time"][11:16]}\n'
                                          f'Читать новость - {short.tinyurl.short(news_api[i]["url"])}')
    else:  # если что-то пошло не так, выводим в консоль ошибку
        update.message.reply_text('Техническая ошибка. Повторите попытку позже.')
        print('Ошибка:')
        print(request)
        print("Http статус:", response.status_code, "(", response.reason, ")")


def contacts(update, context):  # команда выдаёт пользователю мои ФИ и способы связаться
    update.message.reply_text('Семенихин Арсений\nvk - https://vk.com/arssemenikhin\ntg - @arrssenii')


def site(update, context):  # команда выводит сайт проекта
    update.message.reply_text('Сайт проекта - http://kirillka00.pythonanywhere.com/home')


def currate(update, context):  # команда выводит актуальный курс валют
    response = requests.get("https://www.cbr-xml-daily.ru/daily_json.js")  # собираем запрос
    currencies = []  # список для хранения данных
    if response.status_code == 200:  # в хорошем случае
        content = response.json()
        data = [i for i in content['Valute']]
        for i in data:
            values = content['Valute'][i]  # отбираем только нужные данные
            name = values['Name']
            value = values['Value']
            charCode = values['CharCode']
            # отбираем только некоторые (интересные) валюты
            if name == 'Доллар США' or name == 'Евро' or name == 'Польский злотый' or name == 'Японских иен'\
                    or name == 'Вон Республики Корея' or name == 'Швейцарский франк'\
                    or name == 'Чешских крон' or name == 'Украинских гривен' or name == 'Китайский юань'\
                    or name == 'Армянских драмов' or name == 'Белорусский рубль' or\
                    name == 'Фунт стерлингов Соединенного королевства' or name == 'Австралийский доллар':
                currencies.append({'CharCode': charCode, 'Value': value})
        text = ''  # заготовка для сообщение
        k = 1  # количество валюты, по умолчанию 1
        if context.args and context.args[0].isdigit():  # если аргумент был передан
            k = int(context.args[0])
        for i in currencies:
            text += f'{k} {i["CharCode"]} = {round(i["Value"] * k, 2)} RUB\n'
        update.message.reply_text(text)  # выдаём ответ пользователю
    else:  # если что-то пошло не так, выводим в консоль ошибку
        update.message.reply_text('Техническая ошибка. Повторите попытку позже.')
        print('Ошибка:')
        print(response)
        print("Http статус:", response.status_code, "(", response.reason, ")")


def remove_job_if_exists(name, context):
    """Удаляем задачу по имени.
    Возвращаем True если задача была успешно удалена."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


# Обычный обработчик, как и те, которыми мы пользовались раньше.
def set_timer(update, context):
    """Добавляем задачу в очередь"""
    chat_id = update.message.chat_id
    try:
        # args[0] должен содержать значение аргумента
        # (секунды таймера)
        time = context.args[0].split(':')

        # Добавляем задачу в очередь
        # и останавливаем предыдущую (если она была)
        job_removed = remove_job_if_exists(str(chat_id), context)
        context.job_queue.run_daily(task, datetime.time(hour=int(time[0]), minute=int(time[1])),
                                    context=chat_id, name=str(chat_id))

        text = f'Теперь каждый день в {context.args[0]} вы будете получать свежую новость!'
        if job_removed:
            text += 'Старая рассылка отключена.'
        update.message.reply_text(text)

    except (IndexError, ValueError):
        update.message.reply_text('Использование: /notif_news <время>\n'
                                  'Время в формате 00:00')


def task(context):
    """Выводит сообщение"""
    job = context.job
    # собираем запрос
    request = "https://newsapi.org/v2/top-headlines?country=ru&apiKey=499c7a59bd714f83abbee6644022628e"
    response = requests.get(request)  # Выполняем запрос.
    news_api = []  # список для хранения будущих новостей
    if response:
        json_response = response.json()  # Преобразуем ответ в json-объект
        responce = json_response['articles']  # достаём новости
        for article in responce:  # пробегаемся по ним, собирая всё "по полочкам"
            source = (article['source']['name'])
            title = (article['title'])
            url = article['url']
            news_api.append({'source': source, 'title': title, 'url': url})  # добавляем всё, что нужно, в список
        context.bot.send_message(job.context, text=f'{news_api[0]["title"]}\n'
                                                   f'Источник - {news_api[0]["source"]}\n'
                                                   f'Читать новость - {short.tinyurl.short(news_api[0]["url"])}')
    else:  # если что-то пошло не так, выводим в консоль ошибку
        context.bot.send_message(job.context, text='Техническая ошибка. Повторите попытку позже.')
        print('Ошибка:')
        print(request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
    response = requests.get("https://www.cbr-xml-daily.ru/daily_json.js")
    currencies = []
    if response.status_code == 200:
        content = response.json()
        data = [i for i in content['Valute']]
        for i in data:
            values = content['Valute'][i]
            name = values['Name']
            value = values['Value']
            charCode = values['CharCode']
            if name == 'Доллар США' or name == 'Евро' or name == 'Польский злотый' or name == 'Японских иен' \
                    or name == 'Вон Республики Корея' or name == 'Швейцарский франк' \
                    or name == 'Чешских крон' or name == 'Украинских гривен' or name == 'Китайский юань' \
                    or name == 'Армянских драмов' or name == 'Белорусский рубль' or \
                    name == 'Фунт стерлингов Соединенного королевства' or name == 'Австралийский доллар':
                currencies.append({'CharCode': charCode, 'Value': value})
        text = ''
        for i in currencies:
            text += f'1 {i["CharCode"]} = {round(i["Value"], 2)} RUB\n'
        context.bot.send_message(text)
    else:  # если что-то пошло не так, выводим в консоль ошибку
        context.bot.send_message('Техническая ошибка. Повторите попытку позже.')
        print('Ошибка:')
        print(response)
        print("Http статус:", response.status_code, "(", response.reason, ")")


def unset(update, context):
    """Удаляет задачу, если пользователь передумал"""
    chat_id = update.message.chat_id
    job_removed = remove_job_if_exists(str(chat_id), context)
    text = 'Рассылка отключена' if job_removed else 'Вы не настраивали рассылку'
    update.message.reply_text(text)


def search_news(update, context):  # команда для поиска новости по ключевому слову
    if context.args:  # если ключевое слово было введено
        request = f"https://newsapi.org/v2/everything?language=ru&q={context.args[0]}&sortBy=popularity&searchIn=title"\
                  f"&apiKey=499c7a59bd714f83abbee6644022628e"  # собираем запрос
        response = requests.get(request)  # Выполняем запрос.
        news_api = []  # список для хранения будущих новостей
        if response:
            json_response = response.json()  # Преобразуем ответ в json-объект
            responce = json_response['articles']  # достаём новости
            for article in responce:  # пробегаемся по ним, оставляя только нужное
                source = (article['source']['name'])
                title = (article['title'])
                url = article['url']
                news_api.append({'source': source, 'title': title, 'url': url})  # добавляем всё, что нужно, в список
        if news_api:
            update.message.reply_text(f'{news_api[0]["title"]}\n'
                                      f'Источник - {news_api[0]["source"]}\n'
                                      f'Читать новость - {short.tinyurl.short(news_api[0]["url"])}')
        else:
            if response.json()["totalResults"] == 0:
                update.message.reply_text('Нет результатов.')  # если результатов 0, то сообщаем пользователю
            else:  # если же проблема не в отсутствии результатов, то сообщаем пользователю и пишем в консоль об ошибке
                update.message.reply_text('Техническая ошибка. Попробуйте ввести слово ещё раз или повторите попытку позже.')
                print('Ошибка:')
                print(request)
                print("Http статус:", response.status_code, "(", response.reason, ")")
    else:  # если пользователь не ввёл ключевое слово
        update.message.reply_text('Использование: /search <ключевое слово>')


# кастомная клавиатура
reply_keyboard = [['/fresh_news', '/some_news'],
                  ['/course'], ['/off_notif_news'],
                  ['/site', '/contacts'],
                  ['/help']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)


def main():  # основная функция
    # Создаём объект updater.
    updater = Updater('5316273924:AAFk66ewNhn08ex7Oqu-DIbN35EuvyFGAFg', use_context=True)

    # Получаем из него диспетчер сообщений.
    dp = updater.dispatcher
    # добавляем команды в диспетчер
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", helppy))
    dp.add_handler(CommandHandler("fresh_news", fresh_news))
    dp.add_handler(CommandHandler("some_news", some_news))
    dp.add_handler(CommandHandler("search", search_news))
    dp.add_handler(CommandHandler("course", currate))
    dp.add_handler(CommandHandler("contacts", contacts))
    dp.add_handler(CommandHandler("site", site))
    dp.add_handler(CommandHandler("notif_news", set_timer,
                                  pass_args=True,
                                  pass_job_queue=True,
                                  pass_chat_data=True))
    dp.add_handler(CommandHandler("off_notif_news", unset,
                                  pass_chat_data=True))

    # Запускаем цикл приема и обработки сообщений.
    updater.start_polling()
    # Ждём завершения приложения.
    updater.idle()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()