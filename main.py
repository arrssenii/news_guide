from flask import Flask, request, abort, render_template, redirect, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import os
from data.users import User
from data.users import Posts
from data import db_session
from check_pass import password_check
from forms import RegisterForm, LoginForm
# from api import
# настройки приложения
app = Flask(__name__)
app.config['SECRET_KEY'] = 'o_my_god__secret_key'
# sнастройки для логинменеджера
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


''' Нужно добваить вывод рвботы с API + подумать над заполнением главной страницы '''
@app.route("/")  # главная (домашняя) страница
@app.route("/home")
@login_required
def index():
    return render_template("index.html", title='Home')


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
        db_sess = db_session.create_session()  # проверка на существующий акк
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


''' Нужно написать сreate_post.html, форму для создания статьи '''
@app.route('/create_post', methods=['POST', 'GET'])  # обработчик создания статей
@login_required
def create_post():
    if request.method == 'POST':
        creator = request.form['creator']
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']
        post = Posts(creator=creator, title=title, intro=intro, text=text)
        try:
            db_session.add(post)
            db_session.commit()
            return redirect('/home')
        except:
            return 'Error!'
    else:
        return render_template('сreate_post.html')


''' Дописать post_detail.html '''
@app.route('/posts/<int:id>')  # обработчик просомтра статьи
def post_detail(id):
    post = Posts.query.get(id)
    return render_template('post_detail.html', post=post)


@app.errorhandler(404)  # обработчик ошибок
def page_not_found(e):
    return render_template('404.html'), 404


def main():  # главная функция приложния
    db_session.global_init("db/database.db")
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
    app.run(debug=True)


if __name__ == '__main__':  # запуск приложения
    main()
