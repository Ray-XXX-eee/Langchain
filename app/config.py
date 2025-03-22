# app/config.py
import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
TRIAL_LIMIT = 2  # Maximum documents allowed for trial

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is not set!")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY is not set!")
