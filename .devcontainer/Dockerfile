# Use the official Python slim image
FROM python:3.9-slim

# Set environment variables to prevent Python from buffering outputs
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_DEFAULT_TIMEOUT=120 \
    LC_ALL=C.UTF-8 \
    LANG=C.UTF-8

# Install system dependencies
RUN apt-get update \
    && apt-get install --yes --no-install-recommends \
    gcc \
    g++ \
    build-essential \
    python3-dev \
    chromium \
    chromium-driver \  # <-- Install Chromium and its driver
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy packages.txt and install additional system packages
COPY packages.txt packages.txt
RUN xargs -a packages.txt apt-get install --yes

# Copy the application code
COPY . .

# Expose the port used by Streamlit
EXPOSE 8501

# Default command to run the Streamlit app
CMD ["streamlit", "run", "srt.py"]

# Notes for Docker commands
# docker build --progress=plain --tag pydub:latest .
# docker run -ti -p 8501:8501 --rm pydub:latest /bin/bash
# docker run -ti -p 8501:8501 --rm pydub:latest
# docker run -ti -p 8501:8501 -v ${pwd}:/app --rm pydub:latest
