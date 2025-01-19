# Use the official Python slim image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_DEFAULT_TIMEOUT=120 \
    LC_ALL=C.UTF-8 \
    LANG=C.UTF-8

# Install system dependencies and Chromium
RUN apt-get update \
    && apt-get install --yes --no-install-recommends \
    gcc \
    g++ \
    build-essential \
    python3-dev \
    chromium \
    wget \
    curl \
    unzip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Download and install the correct ChromeDriver version
RUN CHROMIUM_VERSION=$(chromium --version | grep -oP '\d+\.\d+\.\d+') && \
    wget https://chromedriver.storage.googleapis.com/${CHROMIUM_VERSION}/chromedriver_linux64.zip && \
    unzip chromedriver_linux64.zip -d /usr/local/bin && \
    rm chromedriver_linux64.zip

# Set the working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy packages.txt and install additional system packages
COPY packages.txt packages.txt
RUN xargs -a packages.txt apt-get install --yes

# Copy the application code
COPY . .

# Expose the port for Streamlit
EXPOSE 8501

# Default command to run the Streamlit app
CMD ["streamlit", "run", "srt.py"]
