from flask import Flask, render_template, request, url_for, redirect
from flask_mysqldb import MySQL
from dotenv import load_dotenv
import os

app = Flask(__name__, static_url_path='/static')
load_dotenv()
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

#----Pagina principal----#
mysql = MySQL(app)
@app.route('/')
def inicio():
    return redirect(url_for('see'))

#----Ver tareas----#
@app.route('/see_tasks')
def see():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM tasks')
    data = cur.fetchall()
    print(data)  
    return render_template('index.html', tasks=data)

#----Añadir tareas----#
@app.route('/add_task', methods=['POST'])
def add_task():
    if request.method == 'POST':
        nombre = request.form['nombre']
        date = request.form['date']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO tasks (date, nombre, completed) VALUES (%s, %s, %s)',
        (date, nombre, 0))
        mysql.connection.commit()   
    return redirect(url_for('see'))

@app.route('/updateTask/<int:task_id>', methods=['POST'])
def update_task(task_id):
    completed = request.form.get('completed') == 'on' #Obtiene el valor del checkbox on se convierte en un booleano
    cur = mysql.connection.cursor()
    cur.execute('UPDATE tasks SET completed = %s WHERE id = %s', (1 if completed else 0, task_id))
    mysql.connection.commit()
    return redirect(url_for('see'))



if  __name__ == '__main__':
    app.run(port=5000, debug=True)
