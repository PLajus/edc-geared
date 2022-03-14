from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm

app = Flask(__name__)

app.config['SECRET_KEY'] = 'a712441fb8ad5e73230b2a2e0de366f6'

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

@app.route("/login")
def login():
    form = LoginForm()
    return render_template("login.html", title="Sign in", form=form)

if __name__ == "__main__":
    app.run(debug=True)