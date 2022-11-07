from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from .models import Post, User, Comment, Contact
from . import db

views = Blueprint("views", __name__)


@views.route("/")
@views.route("/home")
def home():
    #title = Post.query.all()
    posts = Post.query.all()
    return render_template("home.html", user=current_user, posts=posts)

@views.route("/complain")
def complain():
        contact = Contact.query.all()
     
        return render_template("complain.html", user=current_user, contacts=contact)




@views.route("/about")
def about():
    return render_template("about.html", user=current_user)

@views.route("/contact", methods=['GET', 'POST'])
def contact():
    if request.method == "POST":
        email = request.form.get('email')
        text = request.form.get('text')
        if not text:
                flash('Post cannot be empty', category='error')
        else:
            contact = Contact( email = email, text=text, author = 1)
            db.session.add(contact)
            db.session.commit()
            flash('contact submitted successfully', category='success')
            return redirect(url_for('views.home'))
    elif request.method == "GET":
        return render_template("contact.html", user=current_user)




@views.route("/create-post", methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == "POST":
        #title = request.form.get('title')
        text = request.form.get('text')

        if not text:
            flash('Post cannot be empty', category='error')
        else:
            #title = Post( title = title, author=current_user.id)-->
            post = Post( text=text, author=current_user.id)
            #db.session.add(title)
            db.session.add(post)
            db.session.commit()
            flash('Post created!', category='success')
            return redirect(url_for('views.home'))

    return render_template('create_post.html', user=current_user)


@views.route("/delete-post/<id>")
@login_required
def delete_post(id):
    post = Post.query.filter_by(id=id).first()

    if not post:
        flash("Post does not exist.", category='error')
    elif current_user.id == post.id:
        flash('You do not have permission to delete this post.', category='error')
    else:
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted.', category='success')

    return redirect(url_for('views.home'))

@views.route ("/edit-post/<id>",  methods=['GET', 'POST'])
@login_required
def edit(id):
    if request.method == "POST":
        post = Post.query.filter_by(id=id).first()
        if not post:
            flash("Post does not exist.", category='error')
        elif current_user.id == post.author:
       # flash('You do not have permission to edit this post.', category='error')
    #else:
        #edit.title = request.form['title']
           
            text = request.form.get('text')
            # post = Post( text=text, author=current_user.id)
            post.text = text
            db.session.commit()
           
            flash('Post edited.', category='success')
            return redirect(url_for('views.home'))
    elif request.method == "GET":
        post = Post.query.filter_by(id=id).first()
        if not post:
            flash("Post does not exist.", category='error')
        elif current_user.id != post.author:
            flash('You do not have permission to edit this post.', category='error')
    #else:
        #edit.title = request.form['title']
        
    # return redirect(url_for('edit.html', post = edit))
    return render_template('edit.html', post=post)


@views.route("/posts/<username>")
@login_required
def posts(username):
    user = User.query.filter_by(username=username).first()

    if not user:
        flash('No user with that username exists.', category='error')
        return redirect(url_for('views.home'))

    posts = Post.query.filter_by(author=user.id).all()
    return render_template("posts.html", user=current_user, posts=posts, username=username)

@views.route("/create-comment/<post_id>", methods=['POST'])
@login_required
def create_comment(post_id):
    text = request.form.get('text')

    if not text:
        flash('Comment cannot be empty.', category='error')
    else:
        post = Post.query.filter_by(id=post_id)
        if post:
            comment = Comment(
                text=text, author=current_user.id, post_id=post_id)
            db.session.add(comment)
            db.session.commit()
        else:
            flash('Post does not exist.', category='error')

    return redirect(url_for('views.home'))


@views.route("/delete-comment/<comment_id>")
@login_required
def delete_comment(comment_id):
    comment = Comment.query.filter_by(id=comment_id).first()

    if not comment:
        flash('Comment does not exist.', category='error')
    elif current_user.id != comment.author and current_user.id != comment.post.author:
        flash('You do not have permission to delete this comment.', category='error')
    else:
        db.session.delete(comment)
        db.session.commit()

    return redirect(url_for('views.home'))


