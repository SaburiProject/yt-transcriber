# Use official lightweight Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install ffmpeg
RUN apt-get update && apt-get install -y ffmpeg && apt-get clean

# Copy app files
COPY app.py .

# Expose the port Cloud Run will use
ENV PORT 8080
EXPOSE 8080

# Run the app
CMD ["python", "app.py"]
