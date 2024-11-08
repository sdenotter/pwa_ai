import sqlite3
import os
from flask import Flask, render_template, request, jsonify
import requests

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

    content_data = [
        {'name': item[0], 'text': item[1], 'numeric': item[2]}
        for item in content_items
    ]
    return render_template('content.html', content=content_data, title='Content Page')


@app.route('/clipboard')
def clipboard():
    return render_template('clipboard.html', title='Clipboard Utility')


@app.route('/summarize_text', methods=['POST'])
def summarize_text():
    data = request.get_json()
    text = data.get('text', '')
    # Implement summarization logic here
    summarized_text = "Summarized text would be here."
    return jsonify({'summarized_text': summarized_text})

@app.route('/translate_text', methods=['POST'])
def translate_text():
    data = request.get_json()
    text = data.get('text', '')
    # Implement translation logic here
    translated_text = "Translated text would be here."
    return jsonify({'translated_text': translated_text})

@app.route('/grammar_suggestions', methods=['POST'])
def grammar_suggestions():
    data = request.get_json()
    text = data.get('text', '')
    # Implement grammar suggestion logic here
    suggestions = "Grammar suggestions would be here."
    return jsonify({'suggestions': suggestions})

def call_google_ai_api(system_message, user_prompt):
    combined_prompt = system_message + '\n' + user_prompt

    google_api_url = (
        'https://generativelanguage.googleapis.com/v1beta/models/'
        'gemini-1.5-flash-latest:generateContent'
    )
    api_key = os.environ.get('GOOGLE_API_KEY')  # Get the API key from an environment variable
    headers = {'Content-Type': 'application/json'}
    payload = {
        'contents': [{'parts': [{'text': combined_prompt}]}]
    }

    try:
        response = requests.post(
            f'{google_api_url}?key={api_key}',
            headers=headers,
            json=payload
        )
        response.raise_for_status()
        google_response = response.json()
        # Extract the generated text from the response
        generated_text = (
            google_response.get('candidates', [{}])[0]
            .get('content', {})
            .get('parts', [{}])[0]
            .get('text', '')
        )
        return generated_text
    except requests.exceptions.RequestException as e:
        print(f"Error communicating with Google API: {e}")
        return 'Error communicating with the language model.'

@app.route('/process_clipboard', methods=['POST'])
def process_clipboard():
    data = request.get_json()
    text = data.get('text', '')
    processed_text = text.upper()
    print(processed_text)

    system_message = '''
    Your goal is to evaluate the content that a user is pasting into a text box by giving a 1 to 2 sentence explanation of the data.
    For example,
    1. If the user posts a URL, you could return a brief description of the website inferred from the URL (e.g., Washington Post would be 'News' and more info on a specific URL can be inferred from the remaining text),
    2. If there is code present, give a description of the intent/functionality of the code.
    3. If the text looks like raw data, try to infer column names or data types and give an explanation of what the data represents.
    '''
    generated_text = call_google_ai_api(system_message, 'User Generated Text:\n' + processed_text)

    print(generated_text)
    return jsonify({
        'processed_text': processed_text,
        'llm_response': generated_text
    })


@app.route('/clipboard_next', methods=['POST'])
def clipboard_next():
    data = request.get_json()
    generated_text = data.get('generated_text', '')

    system_message = '''
    Based on the following summary, generate the top 3 most likely actions a user would take next. Provide each action as a concise bullet point.
    '''
    generated_text = call_google_ai_api(system_message, 'Summary:\n' + generated_text)

    # Split the actions into a list
    actions = [
        action.strip('-• ')
        for action in generated_text.strip().split('\n') if action
    ]
    actions = actions[1:]
    print(generated_text)

    # Return the actions to the frontend
    return jsonify({'actions': actions})


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


@app.route('/context_builder')
def context_builder():
    return render_template('context_builder.html', title='Context Builder')


if __name__ == '__main__':
    app.run(debug=True)
