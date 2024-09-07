from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/advice/product", methods=['POST'])
def advice():
    data = request.json
    
    if 'messages' not in session:
        session['messages'] = []
        print()