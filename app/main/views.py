import json
from datetime import datetime

import requests
from flask import render_template, flash, redirect, session, request, url_for

from . import main
from .forms import NameForm, LoginForm, PostForm
from ..models import Post


@main.route('/')
def index():
    params = {
        'api_key': '{API_KEY}',
    }

    r = requests.get('http://loclhost:7444/api/post-service/all/{PROJECT_TOKEN}', params=params)
    return render_template('index.html', movies=json.loads(r.text)['posts'])





@main.route('/post', methods=['GET', 'POST'])
def posts():
    post = request.args['post']
    posts = session['posts']
    return render_template('post.html', post=post)


@main.route('/hello', methods=['GET', 'POST'])
def hello():
    name = None
    form = NameForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
    return render_template('hello.html', form=form, name=name)


@main.route('/admin', methods=['GET', 'POST'])
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
                           providers=main.config['OPENID_PROVIDERS'])



