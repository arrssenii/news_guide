from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm

class RegisterForm(FlaskForm):  # форма регистрации
    email = EmailField('Почта:', validators=[DataRequired()])
    hashed_password = PasswordField('Пароль:', validators=[DataRequired()])
    password_again = PasswordField(
        'Повторите пароль:', validators=[DataRequired()])
    username = StringField('Имя пользваотеля:', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')


class LoginForm(FlaskForm):  # форма входа в профиль
    email = EmailField('Почта:', validators=[DataRequired()])
    password = PasswordField('Пароль:', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class CreateForm(FlaskForm):  # форма создания новости
    title = StringField('Заголовок новсти:', validators=[DataRequired()])
    intro = StringField('Интро:', validators=[DataRequired()])
    text = StringField('Текст новости:', validators=[DataRequired()])
    submit = SubmitField('Опубликовать')