from flask import render_template, url_for, flash, redirect, request
from edcgeared import app
from edcgeared.forms import RegistrationForm, LoginForm
import edcgeared.models

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template("register.html", title="Sign up", form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if (request.method == "GET"):
            return render_template("login.html", title="Sign in", form=form)

    if form.validate_on_submit():
        flash('You have logged in.', 'success')
        return redirect(url_for('index'))
    else:
        flash('Incorrect email or password!', 'danger')
        return render_template("login.html", title="Sign in", form=form)
