from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, logout_user, current_user, login_required
from urllib.parse import urlparse
from werkzeug.utils import secure_filename
import os
from app import db
from app.models.user import User
from app.forms.auth import LoginForm, RegistrationForm, ProfileForm

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password', 'danger')
            return redirect(url_for('auth.login'))
        
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlparse(next_page).netloc != '':
            next_page = url_for('main.index')
        
        flash('Successfully logged in!', 'success')
        return redirect(next_page)
    
    return render_template('auth/login.html', title='Sign In', form=form)

@auth.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            university=form.university.data,
            major=form.major.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        
        flash('Congratulations, you are now registered!', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', title='Register', form=form)

@auth.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm()
    if form.validate_on_submit():
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.bio = form.bio.data
        current_user.university = form.university.data
        current_user.major = form.major.data
        
        if form.profile_image.data:
            filename = secure_filename(form.profile_image.data.filename)
            form.profile_image.data.save(os.path.join(current_app.config['UPLOAD_FOLDER'], 'profiles', filename))
            current_user.profile_image = filename
        
        db.session.commit()
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('auth.profile'))
    elif request.method == 'GET':
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.bio.data = current_user.bio
        form.university.data = current_user.university
        form.major.data = current_user.major
    
    return render_template('auth/profile.html', title='Profile', form=form)