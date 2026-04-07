# Start from official Python Image
FROM python:3.11-slim

# Set Working directory inside the container
# Creates folder called app inside the container
WORKDIR /app  

# Copy requirements first before the rest of thr code, Docker caches all the code and saves time.
COPY requirements.txt .

#Install all dependencies
# --no-cache keeps the container size small
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files in the container
# Copies everything into your app
# First . means the current folder on your machine
# Second . means the current folder inside your container
COPY . .

# Expose the port FASTAPI runs on
EXPOSE 8000

# Command to run the app
# The command that runs when the containers starts
# --host 0.0.0.0 means accept connecstions from anywhere
# Without this, FASTAPI  would only accept connections from inside the container
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000" ]