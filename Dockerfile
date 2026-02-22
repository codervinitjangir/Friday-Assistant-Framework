FROM python:3.10-slim

WORKDIR /app

# Install system dependencies (audio, etc)
# Note: Audio in Docker is tricky. This is a base setup.
RUN apt-get update && apt-get install -y \
    gcc \
    portaudio19-dev \
    python3-dev \
    x11-apps \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Environment variables should be passed at runtime
CMD ["python", "src/main.py", "--headless"]
