import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from edcgeared import app, db, bcrypt
from edcgeared.forms import RegistrationForm, LoginForm, UpdateProfileForm
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
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Incorrect email or password!', 'danger')
            return render_template("login.html", title="Sign in", form=form)

def save_image(form_image):
    """Save users profile image in the file system"""

    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_image.filename)
    image_fn = random_hex + f_ext 
    image_path = os.path.join(app.root_path, 'static/profile_images', image_fn)

    output_size = (125, 125)
    resized_image = Image.open(form_image)
    resized_image.thumbnail(output_size)

    resized_image.save(image_path)

    return image_fn

@app.route("/settings", methods=['GET', 'POST'])
@login_required
def settings():
    form = UpdateProfileForm()

    if form.validate_on_submit():
        if form.image.data:
            image_file = save_image(form.image.data)
            if current_user.image_file != "default.jpg":
                os.remove(app.root_path + '/static/profile_images/' + current_user.image_file)
                current_user.image_file = image_file

        current_user.email = form.email.data
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        db.session.commit()

        flash('Profile updated!', 'success')
        return redirect(url_for('settings'))

    elif request.method == "GET":
        form.email.data = current_user.email
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name

    image_file = url_for("static", filename='profile_images/' + current_user.image_file)

    return render_template("settings.html", title="User settings", 
    image_file=image_file,
    form=form)

@app.route("/logout")
@login_required
def logout():

    logout_user()
    return redirect(url_for('index'))