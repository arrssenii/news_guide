import requests

request = "https://newsapi.org/v2/top-headlines?country=ru&apiKey=499c7a59bd714f83abbee6644022628e"
try:
    # Выполняем запрос.
    response = requests.get(request)
    news_api = []
    if response:
        # Преобразуем ответ в json-объект
        json_response = response.json()
        responce = json_response['articles']
        for article in responce:
            source = (article['source']['name'])
            title = (article['title'])
            url = article['url']
            publishedAt = article['publishedAt']
            urlToImage = article['urlToImage']

            if requests.get(urlToImage).status_code == 200:
                news_api.append({'source': source, 'title': title, 'url': url,
                                'publishedAt': publishedAt, 'urlToImage': urlToImage})

    else:
        print("Ошибка выполнения запроса:")
        print(request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
except Exception:
    pass
