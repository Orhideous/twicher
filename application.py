from flask import Flask, render_template
from flask.ext.assets import Environment
from assets import bundles

app = Flask(__name__)
assets = Environment(app)
assets.register(bundles)


@app.route('/')
def hello_world():
    return render_template("main.html")
