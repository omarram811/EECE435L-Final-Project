# start by pulling the python image
FROM python:3.8-alpine

# Set working directory
WORKDIR /app

# Copy application code to container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the service runs on
EXPOSE 5004

# Run the Flask app
CMD ["python", "sales.py"]