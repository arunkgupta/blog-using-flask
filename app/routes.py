from app import flaskapp
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm, RegisterForm, ProfileForm
from flask_login import current_user, login_user, login_required, logout_user
from app.models import User
from werkzeug.urls import url_parse
from app import db
from datetime import datetime


@flaskapp.route("/")
@flaskapp.route("/home")
@flaskapp.route("/index")
@login_required
def index():
    """
    user={"userName":"Arun"}
    :return: Blog Posts
    """
    posts = [
        {
            'author':
                {
                    'username': 'vetri',
                },
            'body': 'Kuttram paarkil suttram illai'

        },
        {
            'author':
                {
                    'username': 'Arun',
                },
            'body': 'This too shall pass'
        },
        {
            'author':
                {
                    'username': 'arul',
                },
            'body': 'Work Hard and Smart'
        },
        {
            'author':
                {
                    'username': 'mary',
                },
            'body': 'I can do anything'
        }
    ]
    return render_template('index.html', title='Arun\'s Blog', posts=posts)


@flaskapp.route("/login", methods=['GET', 'POST'])
def login():
    """
    checking user is authenticated
    :return: login form
    """

    login_form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if login_form.validate_on_submit():
        user = User.query.filter_by(username=login_form.username.data).first()
        if user is None or not user.check_password(login_form.password.data):
            flash('Your username or Password is incorrect. Please check again')
            return redirect(url_for('login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            return redirect(url_for('index'))
        return redirect(next_page)
    return render_template("Login.html", loginform=login_form)


@flaskapp.route("/logout", methods=['GET', 'POST'])
def logout():
    """
    logging out user
    :return: logout user to index page
    """
    logout_user()
    return redirect(url_for('index'))


@flaskapp.route("/register", methods=['GET', 'POST'])
def register():
    """
    User Registration
    :return: registration form
    """
    register_form = RegisterForm()
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if register_form.validate_on_submit():
        user = User(username=register_form.username.data, email=register_form.email.data)
        user.set_password(register_form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("You are succesfully registered in our Blog! Thanks !!")
        return redirect(url_for('index'))
    return render_template("RegisterForm.html", registerform=register_form)


@flaskapp.route("/user/<username>")
@login_required
def user(username):
    """
    user detail page
    :param username: username of requested user
    :return: user profile page
    """
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {
            'author': user,
            'body': "Abracadabra",
        },
        {
            'author': user,
            'body': "ABCEDEFG",
        }
    ]
    return render_template("profile.html", user=user, posts=posts)


@flaskapp.before_request
def before_request():
    """
    Current user authentication check
    :return: adding last seen timestamp in db
    """
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@flaskapp.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    """
    editing profile
    :return: profile edit form
    """
    profile_form = ProfileForm()
    if profile_form.validate_on_submit():
        user = User.query.get(current_user.id)
        user.about_me = profile_form.aboutme.data
        user.username = profile_form.username.data
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('user', username=current_user.username))
    return render_template('ProfileEdit.html', profileform=profile_form)
