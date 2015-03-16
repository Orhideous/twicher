from flask import Flask, render_template
from flask.ext.restful import Api
from flask.ext.assets import Environment

from assets import bundles
from resources import Quote, QuotesList, Random

app = Flask(__name__)
assets = Environment(app)
api = Api(app)

assets.register(bundles)

api.add_resource(QuotesList, '/quotes')
api.add_resource(Quote, '/quotes/<quote_id>')
api.add_resource(Random, '/quotes/twitchy')


@app.route('/')
def index():
    return render_template("main.html")
