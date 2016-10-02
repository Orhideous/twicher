from os import environ

from flask import Flask, render_template
from flask_restful import Api

from models import storage
from resources import Quote, QuotesList, Random

app = Flask(__name__, static_folder="/static")
app.config.from_object(environ.get('APP_SETTINGS', 'config.Development'))

storage.init_app(app)

api = Api(app)

api.add_resource(QuotesList, '/quotes')
api.add_resource(Quote, '/quotes/<quote_id>')
api.add_resource(Random, '/quotes/twitchy')


@app.route('/')
def index():
    return render_template("index.html")


if __name__ == '__main__':
    app.run()
