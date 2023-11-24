from flask import render_template, url_for, flash, redirect, request
from app.forms import RegistrationForm, LoginForm
from app import app, db, bcrypt
from app.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required



posts = [
    {
        "author": "Lavender",
        "title": "Chapo Beans",
        "ingredients": ["chapo", "beans"],
        "method": ["Make chapos", "cook beans", "serve while hot"],
        "date_posted": "Nov 20, 2023",
        "date_updated": "Nov 22, 2023",
    },
    {
        "author": "Ven",
        "title": "Ugali Beef",
        "ingredients": ["flour", "water", "beef", "onions", "tomatoes", "oil", "salt", "dhania"],
        "method": ["Make ugali", "cook beef", "serve while hot"],
        "date_posted": "Oct 20, 2023",
        "date_updated": "Oct 22, 2023",
    },
]


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account')