import json

from flask import render_template, session, url_for
from flask_login import login_required
from werkzeug.utils import redirect

from app.main.forms import PostForm
from app.models import Post
from app.admin import admin


@admin.route('/', methods=['GET'])
@login_required
def admin_view():
    return


@admin.route('/login', methods=['POST'])
def login():
    return render_template('login.html')


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
