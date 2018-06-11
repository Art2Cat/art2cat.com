import requests
from datetime import datetime
import json
from flask import render_template, flash, redirect, session

from app import app
from app.form import NameForm, LoginForm, PostForm
from app.model.post import Post


@app.route('/')
def index():
    params = {
        'api_key': '{API_KEY}',
    }

    r = requests.get('http://loclhost:7444/api/post-service/all/{PROJECT_TOKEN}', params=params)
    return render_template('index.html', movies=json.loads(r.text)['posts'])


@app.route('/admin/write-post', methods=['GET', 'POST'])
def write_post():
    post = Post('test', 'test', datetime.now(),datetime.now(), 'test', [])
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


@app.route('/post', methods= ['GET', 'POST'])
def posts():
    post=request.args['post']
    posts=session['posts']
    return render_template('post.html', post=post)


@app.route('/hello', methods=['GET', 'POST'])
def hello():
    name = None
    form = NameForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
    return render_template('hello.html', form=form, name=name)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for OpenID="%s", remember_me=%s' %
              (form.openid.data, str(form.remember_me.data)))
        session['name'] = form.name.data
        return redirect('/')
    return render_template('login.html',
                           title='Sign In',
                           form=form,
                           providers=app.config['OPENID_PROVIDERS'])


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500
