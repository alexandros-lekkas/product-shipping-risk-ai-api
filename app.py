from flask import Flask, render_template, request
from chatbot import chat # Importing chatbot logic

# LLM setup
messages = []

app = Flask(__name__)

# Root route rendering front page
@app.route('/')
def index():
    return render_template('index.html')

# API route handling chatbot interaction
@app.route('/ask', methods=['POST'])
def ask():
    user_input = request.form['user_input']
    
    messages, bot_response = chat(user_input, messages)
    
    return render_template('index.html', user_input=user_input, bot_response=bot_response)

if __name__ == '__main__':
    app.run(debug=True)