from datetime import datetime

from flask import render_template, flash, redirect, session
from app import app
from app.form import NameForm, LoginForm


@app.route('/')
def index():
    print(datetime.utcnow())
    return render_template('index.html', current_time=datetime.utcnow())


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
