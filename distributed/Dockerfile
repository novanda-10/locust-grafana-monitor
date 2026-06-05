# Use Python 3.9 as the base image
FROM python:3.9

# Set the working directory
WORKDIR /srv/app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the Locust file to the container
COPY locustfile.py .

# Run Locust by default
ENTRYPOINT ["locust"]