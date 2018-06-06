from flask import Flask
from flask_bootstrap import Bootstrap

DEBUG = True
FLATPAGES_AUTO_RELOAD = DEBUG
FLATPAGES_EXTENSION = '.md'
FLATPAGES_ROOT = 'content'
POST_DIR = 'posts'

app = Flask(__name__, template_folder='templates')
Bootstrap(app)
app.config.from_object(__name__)
app.config.from_object('config')

from app import index

app.register_error_handler(404, index.page_not_found)
app.register_error_handler(500, index.internal_server_error)
