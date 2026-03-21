FROM mcr.microsoft.com/devcontainers/python:3.11

# Set timezone to EST (America/New_York)
ENV TZ=America/New_York
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# System tools
RUN apt-get update && apt-get install -y \
    git \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Optional: faster installs
RUN pip install --upgrade pip

WORKDIR /workspace
