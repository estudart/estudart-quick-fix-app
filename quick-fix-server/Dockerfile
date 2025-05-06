# Base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install build dependencies and other necessary packages
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    libssl-dev \
    libxml2-dev \
    libxslt-dev \
    wget \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy application files
COPY fix_server.py /app/fix_server.py
COPY fix_server.cfg /app/fix_server.cfg
COPY spec/FIXT11.xml /app/spec/FIXT11.xml
COPY spec/FIX50SP2.xml /app/spec/FIX50SP2.xml

# Install Python dependencies
RUN pip install --upgrade pip && pip install quickfix

# Expose the FIX server port
EXPOSE 5000

# Run the server
CMD ["python", "fix_server.py"]
