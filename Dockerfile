# Use the official Python image as base
FROM python:3.8.10-slim
# Set the working directory in the container
WORKDIR /app
# Copy the requirements file into the container at /app
COPY requirements.txt .
# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt
# Copy the current directory contents into the container at /app
COPY . /app
# Expose port 8000
EXPOSE 8000
# Command to run the FastAPI application
CMD ["python", "start_server.py"]
