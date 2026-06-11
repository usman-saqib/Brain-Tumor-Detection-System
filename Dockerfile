FROM python:3.10-slim

WORKDIR /app

# Install system dependencies (removed libgl1-mesa-glx)
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Create necessary directories
RUN mkdir -p /tmp/uploads /tmp/reports

# Expose port
EXPOSE 7860

# Run the application
CMD ["python", "app.py"]