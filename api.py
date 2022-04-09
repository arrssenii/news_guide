import requests

request = "https://newsapi.org/v2/top-headlines?country=ru&apiKey=5d4e4058e8c84af4badd8f726ac7dc6d"

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
        news_api.append({'source': source, 'title': title, 'url': url, 'publishedAt': publishedAt, 'urlToImage': urlToImage})
else:
    print("Ошибка выполнения запроса:")
    print(request)
    print("Http статус:", response.status_code, "(", response.reason, ")")
