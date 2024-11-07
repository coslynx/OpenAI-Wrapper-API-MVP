import unittest
from app import app
import openai
from services.openai_service import OpenAIService

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.openai_service = OpenAIService(app.config['OPENAI_API_KEY'])

    def test_generate_text(self):
        test_prompt = "Write a short story about a cat who loves to play with yarn."
        test_model = "text-davinci-003"
        response = self.app.post('/generate', json={'prompt': test_prompt, 'model': test_model})
        self.assertEqual(response.status_code, 200)
        self.assertIn('response', response.json)
        self.assertIsNotNone(response.json['response'])

    def test_generate_text_with_invalid_model(self):
        test_prompt = "Write a short story about a cat who loves to play with yarn."
        test_model = "nonexistent_model"
        response = self.app.post('/generate', json={'prompt': test_prompt, 'model': test_model})
        self.assertEqual(response.status_code, 500)
        self.assertIn('error', response.json)
        self.assertIsNotNone(response.json['error'])

    def test_generate_text_with_empty_prompt(self):
        test_prompt = ""
        test_model = "text-davinci-003"
        response = self.app.post('/generate', json={'prompt': test_prompt, 'model': test_model})
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json)
        self.assertIsNotNone(response.json['error'])

    def test_generate_text_with_malicious_prompt(self):
        test_prompt = "**Bad input!**"
        test_model = "text-davinci-003"
        response = self.app.post('/generate', json={'prompt': test_prompt, 'model': test_model})
        self.assertEqual(response.status_code, 200)  # Expect successful response for now, but could handle with specific error
        self.assertIn('response', response.json)  # Response should still be generated

    def test_openai_service_generate_text(self):
        test_prompt = "Write a short story about a cat who loves to play with yarn."
        test_model = "text-davinci-003"
        response = self.openai_service.generate_text(test_prompt, test_model)
        self.assertIsNotNone(response)
        self.assertNotEqual(response, "")

if __name__ == '__main__':
    unittest.main()