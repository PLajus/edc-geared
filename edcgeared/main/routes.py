from flask import Blueprint, render_template, request
from edcgeared.models import Post

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/news")
def index():
    """Index"""

    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)

    return render_template("index.html", posts=posts)


@main.route("/reviews")
def reviews():
    """Reviews"""
    return render_template("reviews.html")


@main.route("/bestgear")
def bestgear():
    """Best gear"""
    return render_template("bestgear.html")