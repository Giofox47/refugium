from datetime import datetime, timedelta, date
from time import time  # Import fehlte für die Verwendung in get_reset_password_token
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from app import app, db, login

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    name = db.Column(db.String(100), nullable=True)  # Optional hinzugefügt
    surname = db.Column(db.String(100), nullable=True)  # Optional hinzugefügt
    street = db.Column(db.String(100), nullable=True)  # Optional hinzugefügt
    plz = db.Column(db.String(10), nullable=True)  # Optional hinzugefügt
    ort = db.Column(db.String(100), nullable=True)  # Optional hinzugefügt
    land = db.Column(db.String(100), nullable=True)  # Optional hinzugefügt
    telefon = db.Column(db.String(20), nullable=True)  # Optional hinzugefügt
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    buchungen = db.relationship('Buchung', backref='gast', lazy='dynamic')

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')  # Für PyJWT v2.x `.decode('utf-8')` entfernen

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return None
        return User.query.get(id)

class Hutte(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    beschreibung = db.Column(db.String(500), nullable=False)
    preis_pro_nacht = db.Column(db.Float, nullable=False)
    buchungen = db.relationship('Buchung', backref='hutte', lazy='dynamic')

    def __repr__(self):
        return f'<Hütte {self.name}>'

class Buchung(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    check_in = db.Column(db.DateTime, nullable=False)
    check_out = db.Column(db.DateTime, nullable=False)
    gast_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    hutte_id = db.Column(db.Integer, db.ForeignKey('hutte.id'))

    def __repr__(self):
        return f'<Buchung für Hütte {self.hutte.name} von {self.check_in} bis {self.check_out}>'

class Kalender(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    reserved = db.Column(db.Boolean, nullable=True)
    
    def __repr__(self):
        return f'<Startdatum {self.start_date} Enddatum bis {self.end_date}>'

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
