import os
# import dotenv

# pdf_path = "data"
# pdf_files = os.listdir(pdf_path)
# print("PDF Files:", pdf_files)

import os
from dotenv import load_dotenv

# Clear the current environment variables
os.environ.clear()

# Reload from .env
load_dotenv()

# Print values to verify
print("GROQ_API_KEY:", os.getenv("GROQ_API_KEY"))
print("GOOGLE_API_KEY:", os.getenv("GOOGLE_API_KEY"))