from flask import Flask, render_template
from flask_restful import Api

from models import storage
from resources import Quote, QuotesList, Random


def index():
    return render_template("index.html")


def setup_routes(app):
    """Here we map routes to handlers."""

    app.add_url_rule('/', 'index', view_func=index, methods=['GET', 'POST'])


def create_app():
    app = Flask(__name__, static_folder="/static")
    app.config.from_envvar('APP_CONFIG')

    storage.init_app(app)

    api = Api(app)

    api.add_resource(QuotesList, '/quotes')
    api.add_resource(Quote, '/quotes/<quote_id>')
    api.add_resource(Random, '/quotes/twitchy')
    setup_routes(app)

    return app


if __name__ == '__main__':
    create_app().run()
