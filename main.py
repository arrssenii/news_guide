from flask import Flask
from newsapi import NewsApiClient
import requests

newsapi = NewsApiClient(api_key='5d4e4058e8c84af4badd8f726ac7dc6d')

response = newsapi.get_everything(q='bitcoin',
                                  language='ru',
                                  sort_by='popularity',
                                  page=1)

print(response)

app = Flask(__name__)

@app.route('/')
@app.route('/news')
def news():
    return f"<a href={response['articles'][0]['url']}>{response['articles'][0]['title']}</a>"


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')