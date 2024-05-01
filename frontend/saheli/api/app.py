from flask import Flask, request, jsonify
from flask_cors import CORS
# from rag_llama2 import rag

app = Flask(__name__)
CORS(app) 

@app.route('/api/generate', methods=['POST'])
def generate_response():
    data = request.json
    query = data.get('query')

    if not query:
        return jsonify({'error': 'query not provided'}), 400

    # response = rag(query)
    response="po myre"
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=False,host="0.0.0.0",port=8000)
