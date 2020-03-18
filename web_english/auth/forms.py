from flask_wtf import FlaskForm
from web_english.generics.forms import GenericForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, ValidationError

class LoginForm(GenericForm):
    username = StringField("Имя пользователя", validators=[DataRequired()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    submit = SubmitField("Вход", validators=[DataRequired()])

class RegisterForm(GenericForm):
    username = StringField("Имя пользователя", validators=[DataRequired()])
    first_name = StringField("Имя")
    last_name = StringField("Фамилия")
    email = StringField("e-mail", validators=[DataRequired()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    repeat_password = PasswordField("Повторите пароль", validators=[DataRequired()])
    submit = SubmitField("Отправить", validators=[DataRequired()])

    def validate_repeat_password(self, field):
        if field.data != self.password.data:
            raise ValidationError("Пароли не одинаковые")
