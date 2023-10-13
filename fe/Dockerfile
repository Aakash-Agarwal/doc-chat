# Use the official Python image from the Docker Hub
FROM python:3.10

# Create and set the working directory
WORKDIR /app

# Copy the requirements file to the working directory
COPY . /app/

# Expose the port on which your Django app will run
EXPOSE 7000

# Run the Django development server
CMD ["python", "-m", "http.server", "7000"]