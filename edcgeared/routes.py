from flask import render_template, url_for, flash, redirect, request
from edcgeared import app, db, bcrypt
from edcgeared.forms import RegistrationForm, LoginForm
import edcgeared.models
from flask_login import login_user, current_user, logout_user, login_required

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/news")
def news():
    return render_template("news.html")

@app.route("/reviews")
def reviews():
    return render_template("reviews.html")

@app.route("/bestgear")
def bestgear():
    return render_template("bestgear.html")

@app.route("/register", methods=['GET', 'POST'])
def register():
    """Process register API calls"""

    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()

    if form.validate_on_submit():

        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = edcgeared.models.User(first_name=form.first_name.data, last_name=form.last_name.data,
        email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template("register.html", title="Sign up", form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    """Process log in API calls"""

    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()

    if (request.method == "GET"):
            return render_template("login.html", title="Sign in", form=form)

    if form.validate_on_submit():
        user = edcgeared.models.User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash('You have logged in.', 'success')
            return redirect(url_for('index'))
        else:
            flash('Incorrect email or password!', 'danger')
    return render_template("login.html", title="Sign in", form=form)

@app.route("/settings")
@login_required
def settings():
    return render_template("settings.html", title="User settings")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


# TODO: finish
# @app.route('/user', methods=['GET'])
# def get_user():

#     args = request.args
#     email = args.get('email')

#     if email is not None:
#         result = {key: value for key, value in db_users.items() if key == email}
  
#     return result

# @app.route('/category', methods=['GET'])
# def get_user():

#     args = request.args
#     category = args.get('category')

#     if category is not None:
#         result = {key: value for key, value in db_users.items() if key == email}
  
#     return result

