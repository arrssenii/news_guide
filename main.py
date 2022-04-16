from flask import Flask, request, abort, render_template, redirect, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import os
import base64
from data.users import User
from data.news import News
from data import db_session
from check_pass import password_check
from forms import RegisterForm, LoginForm, CreateForm
from work_with_api.news_api import news_api
from work_with_api.currencies_api import currencies
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
    news = db_sess.query(News).filter(News.creator == current_user.username)
    return render_template("index.html", title='Главная', news=news[::-1], news_api=news_api, currencies=currencies)


@app.route("/news_to_me")
@login_required
def news_to_me():
    db_sess = db_session.create_session()
    news = db_sess.query(News).filter(News.creator == current_user.username)
    return render_template("news_to_me.html", title='Ваши новости', news=news[::-1])


@app.route("/news_of_all")
@login_required
def news_of_all():
    db_sess = db_session.create_session()
    news = db_sess.query(News)
    return render_template("news_of_all.html", title='Другие новости', news=news[::-1])


@app.route('/register', methods=['GET', 'POST'])  # обработка регистрации пользователя
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
    db_sess = db_session.create_session()
    news = db_sess.query(News)
    form = CreateForm()
    if form.validate_on_submit():
        image = request.files['file']
        bytestring = image.read()
        if bytestring:
            image = base64.b64encode(bytestring).decode('utf-8')
        else:
            with open('static\img\emptiness.jpg','rb') as file:
                bytestring = file.read()
                image = base64.b64encode(bytestring).decode('utf-8')
        news = News(
            creator = current_user.username,
            title=form.title.data,
            intro=form.intro.data,
            text=form.text.data,
            image=image,
        )  # добавление пользователя в базу
        db_sess.add(news)
        db_sess.commit()
        # переброс пользователя на страницу входа в профиль
        return redirect('/news_to_me')
    return render_template('create_news.html', title='Создание новости', form=form, news=news[::-1])


@app.route('/news/<int:id>')  # обработчик просомтра новости
def news_detail(id):
    db_sess = db_session.create_session()
    news = db_sess.query(News)
    news_title = db_sess.query(News).filter(News.id == id).first()
    return render_template('news_detail.html', title=news_title.title, news=news[::-1], id=id)


@app.errorhandler(404)  # обработчик ошибок
def page_not_found(e):
    return render_template('404.html', title='404'), 404


@app.route('/news_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def news_delete(id):
    db_sess = db_session.create_session()
    news = db_sess.query(News).filter(News.id == id,
                                          News.creator == current_user.username
                                          ).first()
    if news:
        db_sess.delete(news)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/news_to_me')


@app.route('/news_edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_news(id):
    form = CreateForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        news = db_sess.query(News).filter(News.id == id,
                                          News.creator == current_user.username
                                          ).first()
        if news:
            news.creator = current_user.username
            news.title = form.title.data
            news.intro = form.intro.data
            news.image = news.image
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        news = db_sess.query(News).filter(News.id == id,
                                          News.creator == current_user.username
                                          ).first()
        if news:
            image = request.files['file']
            bytestring = image.read()
            if bytestring:
                image = base64.b64encode(bytestring).decode('utf-8')
            else:
                with open('static\img\emptiness.jpg','rb') as file:
                    bytestring = file.read()
                    image = base64.b64encode(bytestring).decode('utf-8')
            news.creator = current_user.username
            news.title = form.title.data
            news.intro = form.intro.data
            news.image = image
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    db_sess = db_session.create_session()
    news = db_sess.query(News)
    return render_template('create_news.html',
                           title='Редактирование Новости',
                           form=form, news=news[::-1])


if __name__ == '__main__':  # запуск приложения
    db_session.global_init("db/database.db")
    app.run(debug=True)