from flask import Flask, render_template, request

import psycopg2

app = Flask(__name__)

# Database connection configuration
db_config = {
    'host': 'localhost',
    'database': 'RickAndMorty',
    'user': 'postgres',
    'password': 'root'
}

# Function to retrieve characters from the database based on search text and pagination


def get_characters(search_text, offset, limit):
    conn = psycopg2.connect(**db_config)
    cur = conn.cursor()

    # Perform the search query
    cur.execute("SELECT * FROM character WHERE name ILIKE %s LIMIT %s OFFSET %s",
                ('%' + search_text + '%', limit, offset))

    characters = cur.fetchall()

    cur.close()
    conn.close()

    return characters

# Route to the index page


@app.route('/')
def index():
    return render_template('index.html')

# Route to the character page


@app.route('/character', methods=['GET', 'POST'])
def character():
    if request.method == 'POST':
        search_text = request.form['search_text']
        offset = 0  # Initial offset for pagination
    else:
        search_text = request.args.get('search_text')
        offset = int(request.args.get('offset', 0))

    limit = 20  # Number of characters to retrieve

    characters = get_characters(search_text, offset, limit)

    prev_offset = max(offset - limit, 0)
    next_offset = offset + limit

    return render_template('character.html', characters=characters, prev_url=f'/character?search_text={search_text}&offset={prev_offset}', next_url=f'/character?search_text={search_text}&offset={next_offset}')


if __name__ == '__main__':
    app.run(debug=True)
