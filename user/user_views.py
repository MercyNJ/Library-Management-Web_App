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
