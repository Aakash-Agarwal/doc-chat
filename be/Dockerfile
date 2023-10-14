# Use the official Python image from the Docker Hub
FROM python:3.10

# Create and set the working directory
WORKDIR /app

# Copy the requirements file to the working directory
COPY . /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port on which your Django app will run
EXPOSE 8000

# Run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]