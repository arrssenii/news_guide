from flask import Flask


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route("/")
def index():
    return 'light tracker'


def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()