from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html', title='Utilities Dashboard')

@app.route('/content')
def content():
    # Connect to the SQLite database
    with sqlite3.connect('database.db') as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT name, text, numeric FROM content")
        content_items = cursor.fetchall()
    content_data = [{'name': item[0], 'text': item[1], 'numeric': item[2]} for item in content_items]
    return render_template('content.html', content=content_data, title='Content Page')

@app.route('/clipboard')
def clipboard():
    return render_template('clipboard.html', title='Clipboard Utility')

@app.route('/calendar')
def calendar():
    return render_template('calendar.html', title='Calendar')

@app.route('/requirements')
def requirements():
    return render_template('requirements.html', title='Requirements Utility')

@app.route('/notes')
def notes():
    return render_template('notes.html', title='Notes')

@app.route('/tasks')
def tasks():
    return render_template('tasks.html', title='Task Manager')

@app.route('/converter')
def converter():
    return render_template('converter.html', title='File Converter')

if __name__ == '__main__':
    app.run(debug=True)