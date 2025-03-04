# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the chatbot_framework package first
COPY . /chatbot_framework

# Copy the API files
COPY . /chatbot_api

# Set the Python path to include the root directory
ENV PYTHONPATH=/

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run the application
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]