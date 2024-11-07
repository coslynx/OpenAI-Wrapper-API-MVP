import os
from dotenv import load_dotenv

# Load Environment Variables
load_dotenv()

# Define Configuration Settings as a Dictionary
class Config:
    # General Settings
    DEBUG = os.getenv("DEBUG", False)  # Enable Debug Mode if DEBUG=True in .env
    TESTING = os.getenv("TESTING", False)  # Enable Testing Mode if TESTING=True in .env
    
    # OpenAI API Configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # Load from the .env file
    DEFAULT_MODEL = "text-davinci-003"  # Default OpenAI Model to use if not specified
    
    # Database Configuration (If used)
    DATABASE_URI = os.getenv("DATABASE_URI")  # Load from the .env file if using a database

    # Logging Settings
    LOGGING_LEVEL = os.getenv("LOGGING_LEVEL", "INFO")  # Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)

# Define Configurations for Different Environments (If necessary)
class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = True

class TestingConfig(Config):
    TESTING = True

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False

# Assign configurations based on the environment (OS environment variable)
config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}