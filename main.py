from flask import Flask, request, abort, render_template, redirect, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import os
import base64
from data.users import User
from data.news import News
from data import db_session
from check_pass import password_check
from forms import RegisterForm, LoginForm
from api import news_api
from currencies_api import currencies
# настройки приложения
app = Flask(__name__)
app.config['SECRET_KEY'] = 'o_my_god__secret_key'
# sнастройки для логинменеджера
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@app.route("/")  # главная (домашняя) страница
@app.route("/home")
@login_required
def index():
    db_sess = db_session.create_session()
    news = db_sess.query(News)
    return render_template("index.html", title='Home', news=news[::-1], news_api=news_api[:6], currencies=currencies)


@app.route("/news_to_me")
@login_required
def news_to_me():
    db_sess = db_session.create_session()
    news = db_sess.query(News)
    return render_template("news_to_me.html", title='Home', news=news[::-1])

# обработка регистрации пользователя
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        check_password = password_check(
            form.hashed_password.data)  # проверка пароля
        if True in check_password.values():
            for k, v in check_password.items():
                if str(v) == 'True':  # вывод конкретной "неправильности" пароля
                    return render_template('register.html', title='Регистрация',
                                           form=form, message=k)
        if form.hashed_password.data != form.password_again.data:  # проверка сходства паролей
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        # проверка на существующий акк
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть!")
        user = User(
            username=form.username.data,
            email=form.email.data,
        )  # добавление пользователя в базу
        user.set_password(form.hashed_password.data)
        db_sess.add(user)
        db_sess.commit()
        # переброс пользователя на страницу входа в профиль
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])  # вход в профиль
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(
            User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильная почта или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')  # обработчик выхода из профиля
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/create_news', methods=['POST', 'GET'])
@login_required
def create_news():
    if request.method == 'POST':
        creator = current_user.username
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']
        image = request.files['file']
        bytes = image.read()

        newimage = base64.b64encode(bytes).decode('utf-8')
        db_sess = db_session.create_session()
        if db_sess.query(News).filter(News.title == title).first():
            return render_template('create_news.html', title='Создание новости',
                                   message="Такая новость уже есть!")
        else:
            new = News(creator=creator, title=title,
                       intro=intro, text=text, image=newimage)
            try:
                db_sess = db_session.create_session()
                db_sess.add(new)
                db_sess.commit()
                return redirect('/news_to_me')
            except Exception as e:
                print(str(e))
                return abort(404)
    else:
        return render_template('create_news.html', title='Создание новости')


@app.route('/news/<int:id>')  # обработчик просомтра новости
def news_detail(id):
    db_sess = db_session.create_session()
    news = db_sess.query(News).filter(News.id == id)
    return render_template('news_detail.html', news=news)


@app.errorhandler(404)  # обработчик ошибок
def page_not_found(e):
    return render_template('404.html', title='404'), 404


def main():  # главная функция приложния
    db_session.global_init("db/database.db")
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
    app.run(debug=True)


if __name__ == '__main__':  # запуск приложения
    main()
