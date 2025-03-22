# Dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app code
COPY . .

# Expose the port (optional for Streamlit)
EXPOSE 8501

# Command to run the app
CMD ["streamlit", "run", "app/main.py", "--server.enableCORS", "false"]
