from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for
from werkzeug import check_password_hash, generate_password_hash
from app import db
from app.auth.forms import LoginForm, RegistrationForm, ResetPasswordRequestForm, ResetPasswordForm
from app.auth.models import User
from flask_login import login_user, logout_user, current_user
from app.auth.email import send_password_reset_email

auth = Blueprint('auth', __name__, url_prefix='/auth')

@auth.route('/login', methods=['GET','POST'])
def login():

    form = LoginForm(request.form)

    if form.validate_on_submit():

        user = User.query.filter_by(username=form.username.data).first()

	if user and check_password_hash(user.password, form.password.data):
	    session['user_id'] = user.id
	    flash("Welcome " + user.name)

	    return redirect(url_for('main.index'))

	flash('Wrong email or password')

    return render_template('auth/login.html', form=form)

@auth.route('/register', methods=['GET', 'POST'])
def register():

    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(name=form.name.data, username=form.username.data, email=form.email.data)
	user.set_password(form.password.data)

	db.session.add(user)
	db.session.commit()

	flash('Account created!')
	return redirect(url_for('auth.login'))

    return render_template('auth/register.html', title='Create Account', form=form)

@auth.route('/reset_password_request', methods=['GET','POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
	if user:
	    send_password_reset_email(user)
	flash('Check your email for password reset instructions')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password_request.html', title = 'Reset Password', form=form)

@auth.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('main.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
	db.session.commit()
	flash('Your password has been reset.')
	return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))
