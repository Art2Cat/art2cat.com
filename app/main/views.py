import json

import requests
from flask import render_template, flash, redirect, session, request, url_for

from app.main import main
from app.main.forms import NameForm, LoginForm


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/blog/', methods=['GET', 'POST'])
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

