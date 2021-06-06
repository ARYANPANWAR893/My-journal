from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from .models import *
from . import db

auth = Blueprint(__name__, 'auth')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if user.password == password:
                login_user(user, remember=True)
                return redirect(url_for('website.routes.home'))
            else:
                return redirect(url_for('website.auth.signup'))
        else:
            return redirect(url_for('website.auth.signup'))

    return render_template('login.html')


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        new_user = User(name=name, username=username,
                        email=email, password=password, bio="Bio!", dp='person.jpg')
        db.session.add(new_user)
        db.session.commit()

        user = User.query.filter_by(email=email).first()
        login_user(user, remember=True)
        return redirect(url_for('website.routes.home'))

    return render_template('signup.html')


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))