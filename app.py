from flask import Flask, render_template, request

import psycopg2

app = Flask(__name__)


def get_characters(search_text, offset, limit):
    try:
        connection = psycopg2.connect(
            host='localhost',
            database='RickAndMorty',
            user='postgres',
            password='root'
        )
    except (Exception, psycopg2.Error) as error:
        print("Erro ao conectar ao PostgreSQL:", error)
    cur = connection.cursor()

    # Query search on postgres database
    cur.execute("SELECT * FROM character WHERE name ILIKE %s LIMIT %s OFFSET %s",
                ('%' + search_text + '%', limit, offset))

    characters = cur.fetchall()

    cur.close()
    connection.close()

    return characters


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/character', methods=['GET', 'POST'])
def character():
    if request.method == 'POST':
        search_text = request.form['search']
        offset = 0
    else:
        search_text = request.args.get('search')
        offset = int(request.args.get('offset', 0))

    limit = 20

    characters = get_characters(search_text, offset, limit)

    prev_offset = max(offset - limit, 0)
    next_offset = offset + limit

    return render_template('character.html', characters=characters, prev_url=f'/character?search={search_text}&offset={prev_offset}', next_url=f'/character?search={search_text}&offset={next_offset}')


if __name__ == '__main__':
    app.run(debug=True)
