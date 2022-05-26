import requests
from datetime import datetime
def api_func(request):
    response = requests.get(request)  # Выполняем запрос.
    news_api = []  # список для хранения будущих новостей
    if response:
        json_response = response.json()  # Преобразуем ответ в json-объект
        responce = json_response['articles']  # достаём новости
        for article in responce:  # пробегаемся по ним, собирая всё "по полочкам"
            source = article['source']['name']
            title = article['title']
            url = article['url']
            publishedAt = article['publishedAt']
            form_publishedAt = datetime.fromisoformat(publishedAt[:-1])
            news_api.append({'source': source, 'title': title, 'url': url,
                            'publishedAt': form_publishedAt.strftime('%d %B | %H:%M')})  # добавляем всё, что нужно, в список
    else:  # если что-то пошло не так, выводим в консоль ошибку
        print("Ошибка выполнения запроса:")
        print(request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
    return news_api

news_api = (api_func('https://newsapi.org/v2/top-headlines?country=ru&apiKey=499c7a59bd714f83abbee6644022628e'))
news_api_tech = (api_func('https://newsapi.org/v2/top-headlines?country=ru&category=technology&apiKey=499c7a59bd714f83abbee6644022628e'))
