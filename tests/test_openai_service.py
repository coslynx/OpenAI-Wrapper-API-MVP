import unittest
from services.openai_service import OpenAIService
import openai
from unittest.mock import patch
from unittest import mock
import os

class TestOpenAIService(unittest.TestCase):

    def setUp(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.openai_service = OpenAIService(self.api_key)

    @patch('services.openai_service.openai.Completion.create')
    def test_generate_text_success(self, mock_create):
        mock_create.return_value = mock.MagicMock(
            choices=[mock.MagicMock(text="This is a mock response.")],
        )
        test_prompt = "Write a short story about a cat who loves to play with yarn."
        test_model = "text-davinci-003"
        response = self.openai_service.generate_text(test_prompt, test_model)
        self.assertEqual(response, "This is a mock response.")

    @patch('services.openai_service.openai.Completion.create')
    def test_generate_text_invalid_model(self, mock_create):
        mock_create.side_effect = openai.error.APIError("Model not found")
        test_prompt = "Write a short story about a cat who loves to play with yarn."
        test_model = "nonexistent_model"
        with self.assertRaises(Exception) as context:
            self.openai_service.generate_text(test_prompt, test_model)
        self.assertEqual(str(context.exception), "Error during OpenAI API call")

    def test_generate_text_empty_prompt(self):
        test_prompt = ""
        test_model = "text-davinci-003"
        with self.assertRaises(Exception) as context:
            self.openai_service.generate_text(test_prompt, test_model)
        self.assertEqual(str(context.exception), "Error during text generation")

    def test_generate_text_malicious_prompt(self):
        test_prompt = "**Bad input!**"
        test_model = "text-davinci-003"
        response = self.openai_service.generate_text(test_prompt, test_model)
        self.assertIsNotNone(response)
        self.assertIn('response', response)

    @patch('services.openai_service.openai.Completion.create')
    def test_generate_text_api_error(self, mock_create):
        mock_create.side_effect = openai.error.APIError("Rate limit exceeded")
        test_prompt = "Write a short story about a cat who loves to play with yarn."
        test_model = "text-davinci-003"
        with self.assertRaises(Exception) as context:
            self.openai_service.generate_text(test_prompt, test_model)
        self.assertEqual(str(context.exception), "Error during OpenAI API call")