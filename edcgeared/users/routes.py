import os

from flask import render_template, url_for, flash, redirect, request, Blueprint, current_app
from flask_login import login_user, current_user, logout_user, login_required
from edcgeared import db, bcrypt
from edcgeared.users.forms import RegistrationForm, LoginForm, UpdateProfileForm
from edcgeared.models import User, Post
from edcgeared.users.utils import save_profile_image

users = Blueprint('users', __name__)

@users.route("/register", methods=['GET', 'POST'])
def register():
    """Registration"""

    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(first_name=form.first_name.data, last_name=form.last_name.data,
        email=form.email.data, password=hashed_password)

        db.session.add(user)
        db.session.commit()

        flash('Account created successfully!', 'success')
        return redirect(url_for('users.login'))

    return render_template("register.html", title="Sign up", form=form)


@users.route("/login", methods=['GET', 'POST'])
def login():
    """Log in"""

    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginForm()
 
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash('You have logged in.', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.index'))
        else:
            flash('Incorrect email or password!', 'danger')
            return render_template("login.html", title="Sign in", form=form)

    elif request.method == "GET":
        return render_template("login.html", title="Sign in", form=form)  


@users.route("/settings", methods=['GET', 'POST'])
@login_required
def settings():
    """User account settings"""

    form = UpdateProfileForm()

    if form.validate_on_submit():
        if form.image.data:
            image_file = save_profile_image(form.image.data)
            if current_user.image_file != "default.jpg":
                os.remove(current_app.root_path + '/static/profile_images/' + current_user.image_file)
            current_user.image_file = image_file
 
        current_user.email = form.email.data
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data

        db.session.commit()

        flash('Profile updated!', 'success')
        return redirect(url_for('users.settings'))

    elif request.method == "GET":
        form.email.data = current_user.email
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name

    image_file = url_for("static", filename='profile_images/' + current_user.image_file)

    return render_template("settings.html", title="User settings", 
    image_file=image_file,
    form=form)


@users.route("/logout")
@login_required
def logout():
    """Log out"""

    logout_user()
    return redirect(url_for('main.index'))


@users.route("/user/<string:email>")
def user_posts(email):
    """User posts"""

    user = User.query.filter_by(email=email).first_or_404()
    page = request.args.get('page', 1, type=int)

    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)

    return render_template("user_posts.html", posts=posts, user=user)
