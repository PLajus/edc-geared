import os
from flask import render_template, url_for, flash, redirect, request, abort, Blueprint, current_app
from flask_login import login_required, current_user
from edcgeared.models import Category, Post
from edcgeared.posts.forms import PostForm
from edcgeared import db
from edcgeared.posts.forms import PostForm
from edcgeared.posts.utils import save_post_image

posts = Blueprint('posts', __name__)

@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    """Create new post"""

    form = PostForm()

    form.categories.choices = [(category.id, category.title) for category in Category.query.all()]

    if form.validate_on_submit():
        image_file = "default.jpg"
        
        if form.image.data:
            image_file = save_post_image(form.image.data)

        slug = form.title.data.replace(" ", "-").lower()
        post = Post(title=form.title.data, content=form.content.data, author=current_user, slug=slug, image=image_file)
        categories = db.session.query(Category).filter(Category.id.in_((form.categories.data))).all()
        post.categories = [category for category in categories]

        db.session.add(post)
        db.session.commit()

        return redirect(url_for('main.index'))

    return render_template("create_post.html", title="New post", form=form,
                            legend="New post")

@posts.route("/post/<int:post_id>")
def post(post_id):
    """Read post"""

    post = Post.query.get_or_404(post_id)

    return render_template('post.html', title=post.title, post=post)


@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    """Update post"""

    post = Post.query.get_or_404(post_id)

    if post.author != current_user:
        abort(403)

    form = PostForm()

    form.categories.choices = [(category.id, category.title) for category in Category.query.all()]

    if form.validate_on_submit():
        if form.image.data:
            image_file = save_post_image(form.image.data)
            if post.image != "default.jpg":
                os.remove(current_app.root_path + '/static/post_images/' + post.image)
            post.image = image_file

        post.title = form.title.data
        post.content = form.content.data

        categories = db.session.query(Category).filter(Category.id.in_((form.categories.data))).all()
        post.categories = [category for category in categories]

        db.session.commit()

        flash("Post updated!", "success")
        return redirect(url_for('posts.post', post_id=post_id))

    elif request.method == "GET":
        form.title.data = post.title
        form.content.data = post.content
        form.categories.data = post.categories

    return render_template('create_post.html', title="Update post",
                            form=form, legend="Update post")


@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    """Delete post"""

    post = Post.query.get_or_404(post_id)

    if post.author != current_user:
        abort(403)

    db.session.delete(post)
    db.session.commit()

    flash("Post deleted!", 'success')
    return redirect(url_for('main.index'))
