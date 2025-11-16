# ---- Stage 1: Base image ----
FROM python:3.12-slim AS base

# Set working directory
WORKDIR /app

# Copy dependency list
COPY requirements.txt .

RUN apt-get update && apt-get install -y gcc python3-dev build-essential

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Expose port Cloud Run expects
ENV PORT=8080
ENV PYTHONUNBUFFERED=1
ENV FLASK_ENV=production

# Start Flask app
CMD ["python", "app.py"]
