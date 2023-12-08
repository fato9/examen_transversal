import sqlite3
from flask import Flask, request

app = Flask(__name__)
db_name = 'test.db'

@app.route('/')
def index():
    return 'Welcome to the hands-on lab for an evolution of password systems!'

# Configuración del servidor para almacenar las credenciales
@app.route('/signup/v1', methods=['POST'])
def signup_v1():
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS USER_PLAIN
                 (USERNAME TEXT PRIMARY KEY NOT NULL,
                  PASSWORD TEXT NOT NULL);''')
    conn.commit()

    try:
        c.execute("INSERT INTO USER_PLAIN (USERNAME, PASSWORD) "
                  "VALUES (?, ?)", (request.form['username'], request.form['password']))
        conn.commit()
    except sqlite3.IntegrityError:
        return "username has been registered."

    print('username:', request.form['username'], 'password:', request.form['password'])
    return "signup success"

# Agregar código para verificar credenciales
def verify_plain(username, password):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    query = "SELECT PASSWORD FROM USER_PLAIN WHERE USERNAME = ?"
    c.execute(query, (username,))
    records = c.fetchone()
    conn.close()
    if not records:
        return False
    return records[0] == password

# Agregar código para iniciar sesión
@app.route('/login/v1', methods=['POST'])
def login_v1():
    error = None
    if request.method == 'POST':
        if verify_plain(request.form['username'], request.form['password']):
            error = 'login success'
        else:
            error = 'Invalid username/password'
    else:
        error = 'Invalid Method'
    return error

# Configuración del servidor con puerto 4850 y certificado autofirmado
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4850, ssl_context='adhoc')