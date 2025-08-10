from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, logout_user, login_required, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password): # type: ignore
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)  # type: ignore
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')
    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()  # type: ignore
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:   # type: ignore
            flash('Email must be greater than 3 characters', category='error')
        elif len(first_name) < 2:   # type: ignore
            flash('First Name must be greater than 1 characters', category='error')
        elif password1 != password2:
            flash('Password don\'t match', category='error')
        elif len(password1) < 7:  # type: ignore
            flash('Password must be at least 7 characters', category='error')
        else:
            new_user = User(
                email=email, # type: ignore
                first_name=first_name, # type: ignore
                password=generate_password_hash(password1)  # Remove method parameter or use 'pbkdf2:sha256' # type: ignore
            )
            db.session.add(new_user) # type: ignore
            db.session.commit() # type: ignore
            login_user(new_user, remember=True)  # type: ignore
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))  # type: ignore
            
    return render_template("sign_up.html", user=current_user)
