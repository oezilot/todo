from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Initialize SQLite Database
def init_db():
    with sqlite3.connect('todo.db') as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS todo_list
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, task TEXT NOT NULL)''')
    conn.close()

# Home route to display all tasks
@app.route('/')
def index():
    with sqlite3.connect('todo.db') as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM todo_list')
        tasks = c.fetchall()
    return render_template('index.html', tasks=tasks)

# Route to add a new task
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        task = request.form['task']
        with sqlite3.connect('todo.db') as conn:
            c = conn.cursor()
            c.execute('INSERT INTO todo_list (task) VALUES (?)', (task,))
            conn.commit()
        return redirect(url_for('index'))
    return render_template('add.html')

# Route to delete a task
@app.route('/delete/<int:task_id>')
def delete(task_id):
    with sqlite3.connect('todo.db') as conn:
        c = conn.cursor()
        c.execute('DELETE FROM todo_list WHERE id = ?', (task_id,))
        conn.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()  # Initialize database
    app.run(debug=True)
