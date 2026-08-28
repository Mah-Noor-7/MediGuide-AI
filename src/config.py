import os
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

# OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Model configuration
MODEL_NAME = "gpt-4o-mini"

# Available options for the Streamlit form
GENDER_OPTIONS = ["Female", "Male", "Other", "Prefer not to say"]

DURATION_OPTIONS = [
    "Less than 1 day",
    "1-3 days",
    "4-7 days",
    "1-2 weeks",
    "More than 2 weeks"
]

LANGUAGE_OPTIONS = ["English", "Urdu"]