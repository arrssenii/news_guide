from flask import Flask, request, abort, render_template, redirect, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import requests
from work_with_images import work_image  # работа с изображениями
from data.users import User  # модель пользователя
from data.news import News  # модель новостей
from data import db_session  # БД
from check_pass import password_check  # функция проверки пароля
from forms import RegisterForm, LoginForm, CreateForm, SearchForm  # формы
# работа с новостями на главной странице
from work_with_api.news_api import news_api
# работа с валютами на главной странице
from work_with_api.currencies_api import currencies
# настройки приложения
app = Flask(__name__)
app.config['SECRET_KEY'] = 'o_my_god__secret_key'
# sнастройки для логинменеджера
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@app.route("/")  # обработчик главной (домашней) страницы
@app.route("/home")
@login_required
def index():
    db_sess = db_session.create_session()  # подключение к БД
    # импорт новостей, принадлежащих текущему пользователю
    news = db_sess.query(News).filter(News.creator == current_user.username)
    # возвращение нужного шаблона с данными
    return render_template("index.html", title='Главная', news=news[::-1], news_api=news_api, currencies=currencies)


# обработчик страницы поиска новостей
@app.route("/news_search", methods=['GET', 'POST'])
@login_required
def news_search():
    db_sess = db_session.create_session()  # подключение к БД
    news = db_sess.query(News)  # импорт всех новостей
    news_search_api = []  # список для хранения найденных новостей
    form = SearchForm()  # форма для поиска
    if form.validate_on_submit():  # нажата ли кнопка "Найти"
        # если форма непустая, составляем запрос с данными формы на русском языке и сортируем по популярности (https://newsapi.org/docs/endpoints/everything)
        if form.search.data:
            request = f"https://newsapi.org/v2/everything?language=ru&q={form.search.data}&sortBy=popularity&searchIn=title&apiKey=499c7a59bd714f83abbee6644022628e"
            response = requests.get(request)  # Выполняем запрос.
            if response:  # проверка на пустоту
                json_response = response.json()  # Преобразуем ответ в json-объект
                responce = json_response['articles']  # достаём новости
                for article in responce:  # перебираем их
                    # и раскладываем "по полочкам"
                    source = (article['source']['name'])
                    title = (article['title'])
                    url = article['url']
                    publishedAt = article['publishedAt']
                    news_search_api.append({'source': source, 'title': title, 'url': url,
                                            'publishedAt': publishedAt})  # отправляем полученные данные в список
                if not news_search_api:  # проверка на пустоту
                    return render_template("news_search.html", title='Поиск новостей', news=news[::-1], form=form, message="Ничего не найдено!")
            else:  # возвращаем ошибку, если что-то пошло не так
                print("Ошибка выполнения запроса:")
                print(request)
                print("Http статус:", response.status_code,
                      "(", response.reason, ")")
                return render_template("news_search.html", title='Поиск новостей', news=news[::-1], form=form)
    # возвращаем нужный шаблон с найденными новостями
    return render_template("news_search.html", title='Поиск новостей', news=news[::-1], form=form, news_search_api=news_search_api)


@app.route("/news_to_me")  # обработчик страницы с новостями пользователя
@login_required
def news_to_me():
    db_sess = db_session.create_session()  # подключение к БД
    news = db_sess.query(News).filter(
        News.creator == current_user.username)  # только новости пользователя
    # возврат нужного шаблона с новостями
    return render_template("news_to_me.html", title='Ваши новости', news=news[::-1])


# обработчик страницы с новостями других пользователей
@app.route("/news_of_all")
@login_required
def news_of_all():
    db_sess = db_session.create_session()  # подключение к БД
    news = db_sess.query(News)  # импорт всех новостей
    # возврат нужного шаблона с новостями
    return render_template("news_of_all.html", title='Другие новости', news=news[::-1])


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
        db_sess = db_session.create_session()  # подключение к БД
        # проверка на существующий акк
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть!")
        user = User(
            username=form.username.data,
            email=form.email.data,
        )  # добавление пользователя в базу
        user.set_password(form.hashed_password.data)  # установка пароля
        db_sess.add(user)  # добавляем нового пользователя в БД
        db_sess.commit()  # закрепляем его в БД
        # переброс пользователя на страницу входа в профиль
        return redirect('/login')
    # возврат нужного шаблона с данными
    return render_template('register.html', title='Регистрация', form=form)


@login_manager.user_loader  # подгрузка пользователя
def load_user(user_id):
    db_sess = db_session.create_session()  # подключение к БД
    return db_sess.query(User).get(user_id)  # возвращение нужного пользователя


@app.route('/login', methods=['GET', 'POST'])  # страница входа в профиль
def login():
    form = LoginForm()  # импорт нужной формы
    if form.validate_on_submit():  # нажата ли кнопка
        db_sess = db_session.create_session()  # подключение к БД
        user = db_sess.query(User).filter(
            User.email == form.email.data).first()
        # проверки для доступа к приложению
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильная почта или пароль",
                               form=form)
    # импорт нужного шаблона с нужными данными
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')  # обработчик выхода из профиля
@login_required
def logout():
    logout_user()  # разлогинивание пользователя
    return redirect(url_for('index'))


# страница создания личной новсти
@app.route('/create_news', methods=['POST', 'GET'])
@login_required
def create_news():
    db_sess = db_session.create_session()  # подключение к БД
    news = db_sess.query(News)  # импорт всех новостей
    form = CreateForm()  # импорт нужной формы
    if form.validate_on_submit():
        image = work_image()
        news = News(  # добавление новости в БД
            creator=current_user.username,
            title=form.title.data,
            intro=form.intro.data,
            text=form.text.data,
            image=image,
        )  # добавление пользователя в базу
        db_sess.add(news)
        db_sess.commit()  # закрепляем новсть в БД
        # переброс пользователя на страницу со своими новстями
        return redirect('/news_to_me')
    # импорт нужного шаблона с нужными данными
    return render_template('create_news.html', title='Создание новости', form=form, news=news[::-1])


@app.route('/news/<int:id>')  # обработчик просомтра новости
def news_detail(id):
    db_sess = db_session.create_session()  # подключение к БД
    news = db_sess.query(News)  # импорт всех новостей
    news_title = db_sess.query(News).filter(
        News.id == id).first()  # достаём заглавие новости
    # импорт нужного шаблона с нужными данными
    return render_template('news_detail.html', title=news_title.title, news=news[::-1], id=id)


@app.errorhandler(404)  # обработчик ошибок
def page_not_found(e):
    # если страница не найдена, кидаем пользователя сюда
    return render_template('404.html', title='404'), 404


# обработчик удаления новостей
@app.route('/news_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def news_delete(id):
    db_sess = db_session.create_session()  # подключение к БД
    news = db_sess.query(News).filter(News.id == id,  # достаём нужную новость
                                      News.creator == current_user.username
                                      ).first()
    if news:  # если новость нашлась - удаляем
        db_sess.delete(news)  # удаление из БД
        db_sess.commit()  # закреп
    else:
        abort(404)
    # переадресация туда же, но уже без удалённой новости
    return redirect('/news_to_me')


# обработчик изменения новости
@app.route('/news_edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_news(id):
    form = CreateForm()  # импорт нужной формы
    db_sess = db_session.create_session()  # подключение к БД
    if form.validate_on_submit():
        news = db_sess.query(News).filter(News.id == id,  # достаём нужную новость
                                          News.creator == current_user.username
                                          ).first()
        if news:
            image = work_image()  # работа с изображениями
            news.creator = current_user.username
            news.title = form.title.data
            news.intro = form.intro.data
            news.image = image
            db_sess.commit()  # закрепляем отредактированную новость в БД
            # переадресация на страницу с личными новостями пользователя
            return redirect('/news_to_me')
        else:
            abort(404)  # если что-то пошло не так, выдаём ошибку
    db_sess = db_session.create_session()  # подключение к БД
    news = db_sess.query(News)  # импорт всех новстей
    # импорт нужного шаблона с нужными данными
    return render_template('create_news.html', title='Редактирование Новости', form=form, news=news[::-1])


def main():  # соновная функция приложения
    db_session.global_init("db/database.db")  # инициализация БД
    app.run(debug=True)  # запуск приложения


if __name__ == '__main__':  # старт
    main()
