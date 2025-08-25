FROM python:3.11-slim

# Install system dependencies for pyheif and Pillow
RUN apt-get update && \
    apt-get install -y libheif-dev gcc libffi-dev libjpeg-dev && \
    rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

# Expose port
EXPOSE 8000

# Start the app with gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:8000", "app:app"]