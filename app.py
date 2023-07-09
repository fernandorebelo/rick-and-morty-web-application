from flask import Flask, url_for, request
from flask import render_template
from markupsafe import escape

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/character/')
@app.route('/character/<name>')
def character(name=''):
    return render_template('character.html', name=name)
