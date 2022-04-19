from flask import Blueprint, render_template, request
from edcgeared.models import Post, Category

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/news")
def index():
    """Index"""

    page = request.args.get('page', 1, type=int)
    query = request.args.get('q')

    if query:
        posts = Post.query.filter(Post.title.contains(query) | 
        Post.content.contains(query)).paginate(page=page, per_page=5)
    else:
        posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)


    return render_template("index.html", posts=posts)


@main.route("/reviews")
def reviews():
    """Reviews"""
    
    categories = Category.query.filter(Category.title == "Reviews")

    page = request.args.get('page', 1, type=int)
    posts = Post.query.join(Post.categories).filter(Category.title.in_(category.title for category in categories)).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    
    return render_template("index.html", posts=posts)


@main.route("/bestgear")
def bestgear():
    """Best gear"""
    
    categories = Category.query.filter(Category.title == "Best gear")

    page = request.args.get('page', 1, type=int)
    posts = Post.query.join(Post.categories).filter(Category.title.in_(category.title for category in categories)).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
   
    return render_template("index.html", posts=posts)