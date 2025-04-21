# Base image
FROM python:3.9-slim

# Install Tesseract OCR and clean up
RUN apt-get update && \
    apt-get install -y tesseract-ocr && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy files
COPY . .

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Default Render port (auto-detect)
ENV PORT=10000

# Run the app
CMD ["python", "app.py"]
