from flask import render_template, current_app, request
from flask_sqlalchemy import get_debug_queries

from app.main import main
from app.main.forms import NameForm
from app.models import Post, User


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
    user = User.query.filter_by(id=current_app.config['ADMIN_ID']).first_or_404()
    page = request.args.get('page', 1, type=int)
    pagination = user.posts.order_by(Post.created_by.desc()).paginate(
        page, per_page=current_app.config['POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    return render_template('blog.html', posts=posts, pagination=pagination, user=user)


@main.route('/search', methods=['GET'])
def search():
    # todo add search veiw
    return None


@main.route('/hello', methods=['GET', 'POST'])
def hello():
    name = None
    form = NameForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
    return render_template('hello.html', form=form, name=name)
