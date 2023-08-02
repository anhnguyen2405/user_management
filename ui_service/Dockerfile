# Use an official Python runtime as a base image
FROM python:3.10

# Set the working directory inside the container
WORKDIR /app

# Copy the contents of the ui_service directory to the working directory
COPY . /app

# Install the required Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port that the ui_service will be running on
EXPOSE 5003

# Command to start the ui_service
CMD [ "python", "ui_service.py" ]
