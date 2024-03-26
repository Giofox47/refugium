from threading import Thread
from flask import render_template
from flask_mail import Message
from app import app, mail


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email, args=(app, msg)).start()


def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email('[Refugium] Passwort zurücksetzen',
               sender=app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/reset_password.txt',
                                         user=user, token=token),
               html_body=render_template('email/reset_password.html',
                                         user=user, token=token))


def send_contact_email(name, email, message):
    subject = "Kontaktanfrage von der Website"
    sender = app.config['ADMINS'][0]  # E-Mail des Absenders
    recipients = [app.config['ADMINS'][0]]  # E-Mail des Empfängers
    text_body = render_template('email/contact.txt', name=name, email=email, message=message)
    html_body = render_template('email/contact.html', name=name, email=email, message=message)
    send_email(subject, sender, recipients, text_body, html_body)
