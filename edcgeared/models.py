from datetime import datetime
from edcgeared import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    """Gets user"""

    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    """User DB Model"""

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    first_name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default="'default.jpg")
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"<User: {self.first_name}, {self.last_name}, {self.image_file}>"

Post_Category = db.Table('Post_Category',
    db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
    db.Column('category_id', db.Integer, db.ForeignKey('category.id')))

class Post(db.Model):
    """Post DB Model"""

    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    title = db.Column(db.String(120), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text)
    slug = db.Column(db.String(120), nullable=False)
    categories = db.relationship('Category', secondary=Post_Category, backref="posts", lazy=True)

    def __repr__(self):
        return f"<Post: {self.title}, {self.date_posted}>"

class Category(db.Model):
    """Category DB Model"""

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(75), nullable=False)
    slug = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f"<Category: {self.title}>"
