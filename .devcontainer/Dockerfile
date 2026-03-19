FROM mcr.microsoft.com/devcontainers/python:3.11

# System tools
RUN apt-get update && apt-get install -y \
    git \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Optional: faster installs
RUN pip install --upgrade pip

WORKDIR /workspace
