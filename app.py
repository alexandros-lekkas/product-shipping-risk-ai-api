from flask import Flask, render_template, request
from chatbot import chat

messages = []

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    global messages
    
    user_input = request.form['user_input']
    
    messages, bot_response = chat(user_input, messages)
    
    return render_template('index.html', user_input=user_input, bot_response=bot_response)

if __name__ == '__main__':
    app.run(debug=True)