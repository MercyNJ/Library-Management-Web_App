#!/usr/bin/python3
from . import user_bp
from flask import Flask, render_template, request
from flask import redirect, url_for, flash, current_app
from flask_login import UserMixin, login_user
from flask_login import login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired
from . import login_manager
from models import storage
from models.user import User
import os
import shortuuid

user_ids = [1, 2, 3, 4]
max_length = 20


class LoginForm(FlaskForm):
    """defines a class for loggining in"""
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    login = SubmitField('Login')
    remember = BooleanField('Remember Me')


class ForgotPasswordForm(FlaskForm):
    """defines a class to change password"""
    username = StringField('Username', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired()])
    forgot_password = SubmitField('Submit New Password')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old Password', validators=[DataRequired()])
    changed_password = PasswordField('Changed Password', validators=[DataRequired()])
    change_password = SubmitField('Change Password')


@login_manager.user_loader
def load_user(user_id):
    """fetches the user from the database"""
    return storage.get(User, int(user_id))



@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    """This facilitates the user login process"""
    login_form = LoginForm()
    forgot_password_form = ForgotPasswordForm()

    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data
        user_found = False
        for user_id in user_ids:
            user = load_user(user_id)
            if user and username == user.username:
                user_found = True
                if check_password_hash(user.password, password):
                    login_user(user, remember=login_form.remember.data)
                    return redirect(url_for('user.index'))
                else:
                    flash("Password mismatch")
                    break

        if not user_found:
            flash("Incorrect username")

    return render_template('login.html', login_form=login_form)

@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('user.login'))


@user_bp.route('/forgot_password', methods=['GET', 'POST'])
# @login_required
def forgot_password():
    """"This allows the user to change the password"""
    forgot_password_form = ForgotPasswordForm()
    if forgot_password_form.validate_on_submit():
        username = forgot_password_form.username.data
        new_password = forgot_password_form.new_password.data
        hashed_password = generate_password_hash(new_password)
        users = storage.all(User).values()
        for user in users:
            if user.username == username:
                user.password = hashed_password
                user.save()
                flash("Password changed successfully")
                return redirect(url_for('user.login'))
    return render_template(
        'forgot_password.html', forgot_password_form=forgot_password_form)


@user_bp.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    """"This allows the user to change the password"""
    change_password_form = ChangePasswordForm()
    if change_password_form.validate_on_submit():
        old_password = change_password_form.old_password.data
        new_password = change_password_form.changed_password.data
        user = current_user
        if user and check_password_hash(user.password, old_password):
            user.set_password(new_password)
            user.save()
            flash("Password changed successfully")
            return redirect(url_for('user.index'))
        else:
            flash("Invalid old password. Please try again.")
    return render_template(
        'change_password.html', change_password_form=change_password_form)


@user_bp.route('/')
@login_required
def index():
    """Displays the home page of the website after the user has logged in"""
    return render_template(
        'index.html', user=current_user)


@user_bp.route('/members_listing')
@login_required
def members_listing():
    return redirect(url_for('members.view_members'))


@user_bp.route('/books_listing')
@login_required
def books_listing():
    return redirect(url_for('books.view_books'))


@user_bp.route('/issuance_listing')
@login_required
def issuance_listing():
    return redirect(url_for('issuance.view_issuances'))


@user_bp.route('/statement_listing')
@login_required
def statement_listing():
    return redirect(url_for('statement.view_open_issuances'))


@user_bp.route('/logout')
@login_required
def logout():
    """Logs out the user"""
    logout_user()
    return redirect(url_for('user.login'))
