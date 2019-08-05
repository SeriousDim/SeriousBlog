from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from app.models import User
from flask_babel import lazy_gettext as _l
from flask_babel import _



# форма входа
class LoginForm(FlaskForm):
    username = StringField(_l("Логин"), validators=[DataRequired()])
    password = PasswordField(_l("Пароль"), validators=[DataRequired()])
    remember = BooleanField(_l("Запомнить меня"))
    submit = SubmitField(_l("Войти"), id="submit")



# форма регистрации
class RegistrationForm(FlaskForm):
    username = StringField(_l("Имя пользователя"), validators=[DataRequired()])
    email = StringField(_l("Почта"), validators=[DataRequired(), Email()])
    password = PasswordField(_l("Пароль"), validators=[DataRequired()])
    password2 = PasswordField(
        _l("Повторите пароль"), validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(_l('Создать аккаунт'))

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError(_("Пожалуйста, используйте другое имя пользователя"))

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if not user == None:
            raise ValidationError(_("Этот e-mail уже занят. Пожалуйста, используйте другой"))