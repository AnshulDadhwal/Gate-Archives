from flask import render_template, url_for, flash, redirect, request
from gate import app, db, bcrypt
from gate.forms import RegistrationForm, LoginForm
from gate.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required


post = [
    {
        'title' : 'What is GATE?',
        'content' : 'Graduate Aptitude Test in Engineering is an All-India test authorized and managed in eight regions across the nation. The exam is conducted by the GATE Committee, faculty members from IISc, and seven other IITs on behalf of the Ministry of Human Resources Development, National Coordinating Board, and Department of Education. The purpose of the GATE exam is to test students’ knowledge in subjects like Engineering and Science. The GATE scorecard is also used by multiple PSUs (Public Sector Undertakings) to recruit applicants for distinguished jobs at Indian Oil, GAIL and Hindustan Petroleum, etc.'
    }
]

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=post)

@app.route("/past")
def about():
    return render_template('past.html', title='Past Papers')

@app.route("/register", methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created successfully! You can log in now :)', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Registration', form=form)

@app.route("/login", methods=['GET','POST'])
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
            flash('Login Unsuccessful. Please check email and password!', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account")
@login_required
def account():
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file)