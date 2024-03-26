from datetime import datetime, timedelta
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db, mail
from app.forms import LoginForm, RegistrationForm, EditProfileForm, ResetPasswordRequestForm, ResetPasswordForm, BuchungsForm  
from app.models import User, Hutte, Buchung, Kalender
from app.email import send_email

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.route('/')
@app.route('/index')
def index():
    # Anzeige der verfügbaren Steinhütten
    huetten = Hutte.query.all()
    return render_template('index.html', huetten=huetten)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Ungültiger Benutzername oder Passwort')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Anmelden', form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    buchungen = Buchung.query.filter_by(gast_id=user.id).all()
    return render_template('user.html', user=user, buchungen=buchungen)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Herzlichen Glückwunsch, Sie sind nun registriert!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Registrieren', form=form)

@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Überprüfen Sie Ihre E-Mails, um Ihr Passwort zurückzusetzen')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html', title='Passwort zurücksetzen', form=form)

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Ihr Passwort wurde zurückgesetzt.')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        db.session.commit()
        flash('Ihre Änderungen wurden gespeichert.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
    return render_template('edit_profile.html', title='Profil bearbeiten', form=form)

@app.route('/buchung', methods=['GET', 'POST'])
@login_required
def buchung():
    form = BuchungsForm()
    heute = datetime.now()
    zehn_wochen_später = heute + timedelta(weeks=10)
    
    if form.validate_on_submit():
        check_in = form.check_in_date.data
        check_out = form.check_out_date.data

        # Ermitteln der Verfügbarkeit durch Prüfung gegen existierende Buchungen
        buchungen = Buchung.query.filter(
            Buchung.check_out > check_in, 
            Buchung.check_in < check_out
        ).all()

        # Wenn es Überschneidungen gibt, sind die Daten nicht verfügbar
        if buchungen:
            flash('Die gewählten Daten sind nicht verfügbar. Bitte wählen Sie andere Daten.')
        else:
            neue_buchung = Buchung(check_in=check_in, check_out=check_out, gast_id=current_user.id)
            db.session.add(neue_buchung)
            db.session.commit()
            flash('Ihre Buchung wurde erfolgreich entgegengenommen!')
            return redirect(url_for('index'))# Umleitung auf die Hauptseite oder eine Erfolgsseite
    # Dies könnte verbessert werden, um tatsächlich verfügbare Tage zu berechnen
    verfuegbare_tage = Kalender.query.filter(Kalender.reserved == False, Kalender.start_date >= heute, Kalender.end_date <= zehn_wochen_später).all()
    
    # falls benötigt für die Anzeige im Buchungsformular.
    return render_template('buchung.html', title='Buchung', form=form)

@app.route('/reserviere/<int:kalender_id>', methods=['POST'])
@login_required
def reserviere(kalender_id):
    kalender = Kalender.query.get_or_404(kalender_id)  # Verwende Kalender statt Termin
    if kalender and not kalender.reserved:
        kalender.reserved = True  # Oder eine andere Logik, um den Termin zu reservieren
        db.session.commit()
        flash('Die Reservierung wurde erfolgreich vorgenommen.', 'success')
    else:
        flash('Dieser Termin ist bereits reserviert.', 'danger')
    return redirect(url_for('buchung'))

@app.route('/storniere_buchung/<int:buchung_id>', methods=['POST'])
@login_required
def storniere_buchung(buchung_id):
    buchung = Buchung.query.get_or_404(buchung_id)
    if buchung.gast_id != current_user.id:
        flash('Sie haben keine Berechtigung, diese Buchung zu stornieren.', 'danger')
        return redirect(url_for('index'))

    # Führe die Stornierung durch (z.B. durch Löschen der Buchung oder Aktualisieren eines Statusfeldes)
    db.session.delete(buchung)
    db.session.commit()
    flash('Die Buchung wurde erfolgreich storniert.', 'success')
    return redirect(url_for('user', username=current_user.username))


@app.route('/success')
def success_page():
    return render_template('success.html')

