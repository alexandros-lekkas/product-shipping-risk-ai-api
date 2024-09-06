from flask import Flask, render_template, request, session
from chatbot import chat
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secret key for session

# Helper function to serialize messages
def serialize_messages(messages):
    serialized = []
    for message in messages:
        if isinstance(message, HumanMessage):
            serialized.append({'type': 'human', 'content': message.content})
        elif isinstance(message, AIMessage):
            serialized.append({'type': 'ai', 'content': message.content})
        elif isinstance(message, SystemMessage):
            serialized.append({'type': 'system', 'content': message.content})
    return serialized

# Helper function to deserialize messages
def deserialize_messages(serialized_messages):
    messages = []
    for message in serialized_messages:
        if message['type'] == 'human':
            messages.append(HumanMessage(content=message['content']))
        elif message['type'] == 'ai':
            messages.append(AIMessage(content=message['content']))
        elif message['type'] == 'system':
            messages.append(SystemMessage(content=message['content']))
    return messages

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_input = request.form['user_input']
    
    # Load messages from session and deserialize, or initialize if not available
    if 'messages' not in session:
        session['messages'] = []
        print("Messages not in session")
    messages = deserialize_messages(session['messages'])
    print("Deserialize messages")

    # Chat and get bot response
    messages, bot_response = chat(user_input, messages)
    print(messages)
    print(bot_response)

    # Serialize and update session with the latest messages
    session['messages'] = serialize_messages(messages)

    return render_template('index.html', user_input=user_input, bot_response=bot_response)

if __name__ == '__main__':
    app.run(debug=True)
