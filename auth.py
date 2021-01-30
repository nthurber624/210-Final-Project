from flask import render_template, redirect, request, url_for, Blueprint, flash
from flask_login import login_user, logout_user, login_required, current_user
from forms import LoginForm, RegistrationForm

auth = Blueprint('auth', __name__)

from tables import User

@auth.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user is not None and user.verifyPassword(form.password.data): # if the user already exists and the password works
            login_user(user, form.rememberMe.data)
            return redirect(url_for('index'))
        flash('Invalid email or password.')
    return render_template('login.html', loginForm=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('index'))

from app import db
from emailAuth import sendEmail

@auth.route('/register', methods=['POST', 'GET'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        access = 1
        if form.admin.data == True: # given more access
            access = 2
        user = User(email=form.email.data, name=form.name.data, password=form.password.data, access=access)
        db.session.add(user)
        db.session.commit()

        token = user.generateToken()
        subject = 'Please confirm your email'
        confirmURL = url_for('auth.confirm', token=token, _external=True)
        html = render_template('email/confirm.html', user=user, token=token, confirmURL=confirmURL)
        sendEmail(user.email, subject, html)

        login_user(user)
        flash('A confirmation email has been sent to you by email.')
        return redirect(url_for('index'))
    return render_template('register.html', registrationForm=form)

@auth.before_app_request
def beforeRequest():
    if current_user.is_authenticated and not current_user.confirmed and request.blueprint != 'auth' and request.endpoint != 'static':
        return redirect(url_for('auth.unconfirmed'))

@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('index'))
    return render_template('unconfirmed.html')

@auth.route('/confirm')
@login_required
def resendConfirmation():
    token = current_user.generateToken()
    confirmURL = url_for('auth.confirm', token=token, _external=True)
    sendEmail(current_user.email, 'Please confirm your account', render_template('email/confirm.html', user=current_user, confirmURL=confirmURL))
    flash('A new confirmation email has been sent to you by email.')
    return redirect(url_for('index'))

@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    user = current_user
    if user.confirmed:
        return redirect(url_for('index'))
    if user.confirm(token):
        db.session.commit()
        flash("You have confirmed your account. Thanks!")
    else:
        flash("The confirmation link is invalid or has expired.")
    return redirect(url_for('index'))
