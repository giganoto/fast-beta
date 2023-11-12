# Use an official Python runtime as a parent image
FROM python:3.12.0-slim-bullseye

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install any needed packages specified in requirements.txt
RUN apt-get update && \
    apt-get install -y libpq-dev gcc && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Make port 5000 available to the world outside this container
EXPOSE 8080

# Define environment variable
ENV NAME admin_backend
ENV environment development

# Run main.py when the container launches
CMD ["python", "app.py"]
