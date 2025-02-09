from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Database setup
def init_db():
    with sqlite3.connect('todo.db') as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY AUTOINCREMENT, task TEXT, done INTEGER)''')
        conn.commit()

# Route to display all tasks
@app.route('/')
def index():
    with sqlite3.connect('todo.db') as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM tasks")
        tasks = c.fetchall()
    return render_template('index.html', tasks=tasks)

# Route to add a new task
@app.route('/add', methods=['POST'])
def add_task():
    task = request.form.get('task')
    if task:
        with sqlite3.connect('todo.db') as conn:
            c = conn.cursor()
            c.execute("INSERT INTO tasks (task, done) VALUES (?, ?)", (task, 0))
            conn.commit()
    return redirect(url_for('index'))

# Route to mark task as done
@app.route('/done/<int:task_id>')
def mark_done(task_id):
    with sqlite3.connect('todo.db') as conn:
        c = conn.cursor()
        c.execute("UPDATE tasks SET done = 1 WHERE id = ?", (task_id,))
        conn.commit()
    return redirect(url_for('index'))

# Route to delete a task
@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    with sqlite3.connect('todo.db') as conn:
        c = conn.cursor()
        c.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
