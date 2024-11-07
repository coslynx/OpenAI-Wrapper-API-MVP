from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os

from services.openai_service import OpenAIService

load_dotenv()

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')

openai_service = OpenAIService(os.getenv('OPENAI_API_KEY'))

@app.route('/generate', methods=['POST'])
def generate_text():
    try:
        prompt = request.json.get('prompt')
        model = request.json.get('model', 'text-davinci-003')
        response = openai_service.generate_text(prompt, model)
        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)