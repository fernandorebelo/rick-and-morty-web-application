from flask import Flask, url_for, request
from flask import render_template
from markupsafe import escape

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/character', methods=['GET', 'POST'])
def character():
    if 'back' in request.form:
        return render_template('home.html')

    if request.method == 'POST':
        name = request.form['name']
        return render_template('character.html', name=name)
    else:
        name = request.args.get('name')
        return render_template('character.html', name=name)


if __name__ == '__main__':
    app.run()
