import json

from flask import render_template, session, url_for, flash, request
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.utils import redirect

from app import db
from app.main.forms import PostForm
from app.admin.forms import LoginForm, RegistrationForm
from app.models import Post, User
from app.admin import admin


@admin.route('/', methods=['GET'])
@login_required
def admin_view():
    return


@admin.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid username or password.')
    return render_template('login.html', form=form)


@admin.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User()
        user.email = form.email.data,
        user.username = form.username.data,
        user.password = form.password.data
        db.session.add(user)
        flash('You can now login.')
        return redirect(url_for('admin.login'))
    return render_template('register.html', form=form)


@admin.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


@admin.route('/write-post', methods=['GET', 'POST'])
@login_required
def write_post():
    post = Post()
    form = PostForm()
    if form.validate_on_submit():
        print("done")
        post.title = form.title
        post.article = form.article
        post.tags = form.tags
        posts = json.dumps(post)
        session['posts'] = posts
        return redirect(url_for('/post', posts=posts))
    else:
        return render_template('write-post.html', form=form)
