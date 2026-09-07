FROM python:3.10-slim

# Python settings
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1

# Project directory
WORKDIR /VJ-FILTER-BOT

# System packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        ffmpeg \
        git \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements first for Docker cache
COPY requirements.txt .

# Upgrade pip and install Python packages
RUN python -m pip install --upgrade pip && \
    python -m pip install -r requirements.txt

# Copy complete project
COPY . .

# Start Telegram bot
CMD ["python", "bot.py"]
