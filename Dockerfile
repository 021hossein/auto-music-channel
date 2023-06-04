# Base image with Python
FROM python:3.9-slim

# Install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    ffmpeg \
    openssl \
    aria2 \
    g++ \
    git \
    libffi-dev \
    zlib1g-dev

# Set working directory
WORKDIR /app

# Copy the Python script and requirements.txt
COPY main.py telegram_helper.py /app/
COPY music.mp3 /app/
COPY requirements.txt /app/


# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the Python script
CMD ["python", "main.py"]
