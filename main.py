from flask import Flask
from newsapi import NewsApiClient

newsapi = NewsApiClient(api_key='5d4e4058e8c84af4badd8f726ac7dc6d')


app = Flask(__name__)


@app.route('/')
@app.route('/news')
def news():
    responses = []
    for i in range(5):
        j = i + 1
        response = newsapi.get_everything(q='россия',
                                          language='ru',
                                          sort_by='popularity',
                                          page=j)
        print(response)
        responses.append(response)
    print(responses)
    return f"<a href={responses[0]['articles'][0]['url']}>{responses[0]['articles'][0]['title']}</a></br>"\
           f"<a href={responses[1]['articles'][0]['url']}>{responses[1]['articles'][0]['title']}</a></br>"\
           f"<a href={responses[2]['articles'][0]['url']}>{responses[2]['articles'][0]['title']}</a></br>"\
           f"<a href={responses[3]['articles'][0]['url']}>{responses[3]['articles'][0]['title']}</a></br>"\
           f"<a href={responses[4]['articles'][0]['url']}>{responses[4]['articles'][0]['title']}</a></br>"


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')