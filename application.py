from os import environ

from flask import Flask, render_template
from flask.ext.restful import Api
from flask.ext.assets import Environment

from assets import bundles
from models import db
from resources import Quote, QuotesList, Random

app = Flask(__name__)
app.config.from_object(environ.get('APP_SETTINGS', 'config.Development'))

assets = Environment(app)
api = Api(app)

assets.register(bundles)

api.add_resource(QuotesList, '/quotes')
api.add_resource(Quote, '/quotes/<quote_id>')
api.add_resource(Random, '/quotes/twitchy')


@app.before_first_request
def bind_to_db():
    db.bind(app.config['DB_TYPE'], app.config['DB_NAME'], create_db=False)
    db.generate_mapping()


@app.route('/')
def index():
    return render_template("main.html")

if __name__ == '__main__':
    app.run()
