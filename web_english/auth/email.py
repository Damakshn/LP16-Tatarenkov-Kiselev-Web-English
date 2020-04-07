from web_english.email import send_email
from flask import render_template


def send_password_reset_email(user):
    token = user.get_token()
    send_email('[WE] Сброс пароля',
               recipients=[user.email],
               text_body=render_template('email/reset_password.txt',
                                         user=user, token=token),
               html_body=render_template('email/reset_password.html',
                                         user=user, token=token))


def send_verification_email(user):
    token = user.get_token(expires_in=600)
    send_email('[WE] Подтверждение почты',
               recipients=[user.email],
               text_body=render_template('email/ver_email.txt',
                                         user=user, token=token),
               html_body=render_template('email/ver_email.html',
                                         user=user, token=token))
