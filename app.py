from flask import Flask, request
from flask import render_template
import psycopg2

app = Flask(__name__)


def search_character(text):
    # Database connection
    try:
        connection = psycopg2.connect(
            host='localhost',
            database='RickAndMorty',
            user='postgres',
            password='root'
        )
    except (Exception, psycopg2.Error) as error:
        print("Erro ao conectar ao PostgreSQL:", error)
    # Cria um cursos
    cursor = connection.cursor()
    # Cria sql para pesquisar no banco de dados
    query_name = "SELECT * FROM character WHERE name ILIKE %s OFFSET 0 LIMIT 20"
    cursor.execute(query_name, (f'%{text}%',))
    data = cursor.fetchall()
    # Fecha cursor
    connection.close()
    return data


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        text = request.form.get('text')
        character_data = search_character(text)
        return render_template('character.html', characters=character_data)
    return render_template('home.html')


@app.route('/character')
def character():
    return render_template('character.html', characters=character)


if __name__ == '__main__':
    app.run()
