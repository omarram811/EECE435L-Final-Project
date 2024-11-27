# Start with a Python image
FROM python:3.10-alpine
RUN apk add --no-cache gcc musl-dev python3-dev linux-headers

COPY ./requirements.txt /app/services/sales/requirements.txt

# Set working directory
WORKDIR /app/services/sales

# Install dependencies
RUN pip install -r requirements.txt

# Copy the entire app directory into the container
COPY . /app/

# Expose the port the service runs on
EXPOSE 5004

# Run the Flask app
CMD ["python3", "sales.py"]