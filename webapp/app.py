
from flask import Flask, render_template, request
import requests

# Set up Flask app
app = Flask(__name__)

# Set your OpenAI API key
api_key = "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"

# Define your base URL for OpenAI API
base_url = "https://api.openai.com/v1/models/"

# Define your GPT-3 model
gpt3_model = "text-davinci-001"

# Define a function to generate text based on user input
def generate_text(prompt):
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    payload = {
        "prompt": prompt,
        "max_tokens": 150
    }
    response = requests.post(base_url + gpt3_model + "/completions", headers=headers, json=payload)
    response_json = response.json()
    if 'choices' in response_json and len(response_json['choices']) > 0:
        return response_json['choices'][0]['text'].strip()
    else:
        return "Error: Unable to generate text"

# Define route to list models
@app.route('/list_models')
def list_models():
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    response = requests.get(base_url, headers=headers)
    models = response.json()['data']
    return render_template('list_models.html', models=models)

# Define route to retrieve a specific model instance
@app.route('/retrieve_model/<model_id>')
def retrieve_model(model_id):
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    response = requests.get(base_url + model_id, headers=headers)
    model = response.json()
    return render_template('retrieve_model.html', model=model)

# Define routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    question = request.form['question']
    answer = generate_text(question)
    return render_template('index.html', question=question, answer=answer)

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)

