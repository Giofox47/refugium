from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, \
    TextAreaField, DateField  
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, \
    Length, Regexp
import sqlalchemy as sa
from app import db
from app.models import User


class LoginForm(FlaskForm):
    username = StringField('Benutzername', validators=[DataRequired()])
    password = PasswordField('Passwort', validators=[DataRequired()])
    remember_me = BooleanField('Angemeldet bleiben')
    submit = SubmitField('Anmelden')

class RegistrationForm(FlaskForm):
    username = StringField('Benutzername', validators=[DataRequired()])
    email = StringField('E-Mail', validators=[DataRequired(), Email()])
    password = PasswordField('Passwort', validators=[DataRequired()])
    password2 = PasswordField(
        'Passwort wiederholen', validators=[DataRequired(), EqualTo('password')])
    name = StringField('Vorname', validators=[DataRequired()])
    surname = StringField('Nachname', validators=[DataRequired()])
    street = StringField('Strasse', validators=[DataRequired()])
    plz = StringField('Postleitzahl', validators=[DataRequired(), Regexp(r'^\d{4}$', message='Bitte geben Sie eine gültige Postleitzahl ein.')])
    ort = StringField('Ort', validators=[DataRequired()])
    land = StringField('Land', validators=[DataRequired()])
    telefon = StringField('Telefon', validators=[DataRequired(), Regexp(r'^\+?(\d[\d\- ]+)?(\([\d\- ]+\))?[\d\- ]+\d$', message='Bitte geben Sie eine gültige Telefonnummer ein.')])
    submit = SubmitField('Registrieren')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Bitte wählen Sie einen anderen Benutzernamen.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Bitte verwenden Sie eine andere E-Mail-Adresse.')


class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Passwort zurücksetzen anfordern')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Passwort', validators=[DataRequired()])
    password2 = PasswordField(
        'Passwort wiederholen', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Passwort zurücksetzen anfordern')


class EditProfileForm(FlaskForm):
    username = StringField('Benutzername', validators=[DataRequired()])
    name = StringField('Vorname', validators=[DataRequired()])
    surname = StringField('Nachname', validators=[DataRequired()])
    street = StringField('Strasse', validators=[DataRequired()])
    plz = StringField('Postleitzahl', validators=[DataRequired(), Regexp(r'^\d{5}$', message='Bitte geben Sie eine gültige Postleitzahl ein.')])
    ort = StringField('Ort', validators=[DataRequired()])
    land = StringField('Land', validators=[DataRequired()])
    telefon = StringField('Telefon', validators=[DataRequired(), Regexp(r'^\+?(\d[\d\- ]+)?(\([\d\- ]+\))?[\d\- ]+\d$', message='Bitte geben Sie eine gültige Telefonnummer ein.')])
    submit = SubmitField('Speichern')
    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Bitte wählen Sie einen anderen Benutzernamen.')


class EmptyForm(FlaskForm):
    submit = SubmitField('Bestätigen')


class BuchungsForm(FlaskForm):
    check_in_date = DateField('Check-in Datum', validators=[DataRequired()], format='%Y-%m-%d')
    check_out_date = DateField('Check-out Datum', validators=[DataRequired()], format='%Y-%m-%d')
    submit = SubmitField('Buchen')
    
    