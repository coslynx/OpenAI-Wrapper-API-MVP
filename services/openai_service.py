import openai
import logging
from config import Config
import requests

class OpenAIService:
    def __init__(self, api_key):
        openai.api_key = api_key
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(Config.LOGGING_LEVEL)

    def generate_text(self, prompt, model="text-davinci-003"):
        self.logger.info(f"Generating text with model: {model}, prompt: {prompt}")
        try:
            response = openai.Completion.create(
                engine=model,
                prompt=prompt,
                max_tokens=1024,
                n=1,
                temperature=0.7,
                stop=None,
            )
            self.logger.info(f"OpenAI API response: {response}")
            return response.choices[0].text
        except openai.error.APIError as e:
            self.logger.error(f"OpenAI API Error: {e}")
            raise Exception("Error during OpenAI API call")
        except Exception as e:
            self.logger.error(f"Error during text generation: {e}")
            raise Exception("Error during text generation")