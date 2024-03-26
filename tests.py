from flask import url_for
from datetime import datetime, timedelta
import unittest
from app import app, db
from app.models import User, Hutte, Buchung
from app.forms import BuchungsForm

class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        # Setze die Anwendungskonfiguration auf eine Testdatenbank
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False  # Deaktiviere CSRF für Testzwecke
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = app.test_client(use_cookies=True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_user_registration(self):
        # Teste die Benutzerregistrierung
        response = self.client.post('/register', data={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'test',
            'password2': 'test',
            'name': 'Test',
            'surname': 'User',
            'street': 'Teststrasse',
            'plz': '1234',
            'ort': 'Testort',
            'land': 'Testland',
            'telefon': '+41123456789'
        })
        self.assertEqual(response.status_code, 302)  # Weiterleitung nach erfolgreicher Registrierung

    def test_login(self):
        # Teste den Login
        user = User(username='testuser', email='test@example.com')
        user.set_password('test')
        db.session.add(user)
        db.session.commit()
        
        response = self.client.post('/login', data={
            'username': 'testuser',
            'password': 'test'
        }, follow_redirects=True)
        
        self.assertIn(b'Willkommen', response.data)

    def login(self, username, password):
        return self.client.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.client.get('/logout', follow_redirects=True)

    def test_buchung(self):
        # Erstelle einen Benutzer und melde ihn an
        user = User(username='buchungstester', email='buchung@test.com')
        user.set_password('test')
        db.session.add(user)
        db.session.commit()
        
        self.login('buchungstester', 'test')
        
        # Erstelle eine Hütte für die Buchung
        hutte = Hutte(name='Testhütte', beschreibung='Testbeschreibung', preis_pro_nacht=100)
        db.session.add(hutte)
        db.session.commit()

        # Versuche, eine Buchung zu erstellen
        response = self.client.post('/buchung', data={
            'check_in_date': '2023-01-01',
            'check_out_date': '2023-01-02',
            # Hier musst du möglicherweise die ID der Hütte auf andere Weise übergeben,
            # je nachdem, wie deine Formulare und Routen konfiguriert sind.
            # 'hutte_id': hutte.id  # Wenn die Hutte-ID direkt im Formular benötigt wird
        }, follow_redirects=True)

        self.assertIn(b'Ihre Buchung wurde erfolgreich entgegengenommen!', response.data)
        
        # Melde den Benutzer ab
        self.logout()
    
if __name__ == '__main__':
    unittest.main()
