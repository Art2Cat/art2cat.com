from flask import render_template, flash, redirect, session, request, url_for, current_app
from flask_sqlalchemy import get_debug_queries
from app.main import main
from app.main.forms import NameForm, LoginForm


@main.after_app_request
def after_request(response):
    for query in get_debug_queries():
        if query.duration >= current_app.config['SLOW_DB_QUERY_TIME']:
            current_app.logger.warning(
                'Slow query: %s\nParameters: %s\nDuration: %fs\nContext: %s\n'
                % (query.statement, query.parameters, query.duration,
                   query.context))
    return response


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
