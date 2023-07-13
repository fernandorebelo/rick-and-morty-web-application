from flask import Flask, request
from flask import render_template
import psycopg2

app = Flask(__name__)

# Database connection information
host = 'localhost'
database = 'RickAndMorty'
user = 'postgres'
password = 'root'

try:
    connection = psycopg2.connect(
        host=host,
        database=database,
        user=user,
        password=password
    )
except (Exception, psycopg2.Error) as error:
    print("Erro ao conectar ao PostgreSQL:", error)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/character', methods=['POST'])
def character():
    cursor = connection.cursor()
    name_submit = request.form.get('name')
    query_name = "SELECT * FROM character WHERE name ILIKE %s OFFSET 0 LIMIT 20"
    cursor.execute(query_name, ('%'+name_submit+'%',))
    rows = cursor.fetchall()
    cursor.close()

    return render_template('character.html', rows=rows)


if __name__ == '__main__':
    app.run()
