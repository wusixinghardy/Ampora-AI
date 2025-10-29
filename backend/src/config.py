import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Unified naming — matches your .env file
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-5")