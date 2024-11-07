from flask import request, jsonify
from flask_restful import Resource, Api, reqparse
from services.openai_service import OpenAIService

api = Api()

class GenerateText(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('prompt', type=str, required=True, help="Prompt is required")
        parser.add_argument('model', type=str, required=False, default='text-davinci-003', help="Model can be provided, defaults to 'text-davinci-003'")
        args = parser.parse_args()
        prompt = args['prompt']
        model = args['model']

        try:
            response = OpenAIService.generate_text(prompt, model)
            return jsonify({'response': response}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

api.add_resource(GenerateText, '/generate')

# Add additional routes for other features as needed

# Register the API with your Flask app
from app import app # Import your Flask app instance
api.init_app(app) # Initialize the API with your Flask app