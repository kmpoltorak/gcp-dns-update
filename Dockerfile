# Latest python default docker image
FROM python:latest

# Update and upgrade python image
RUN apt-get update && apt-get upgrade -yq

# Copy app data to docker container
COPY app/ app/

# Change default directory
WORKDIR /app

# Install needed python3 packages
RUN pip3 install -r requirements.txt

# Mandatory environment variables from your GCP project
ENV GCP_PROJECT_ID "your-project-id"
ENV GCP_DNS_ZONE "example-com"
ENV GCP_A_RECORD "domain.example.com."
# Service account credentials environment variable with file generated in GCP console as JSON for GCP API client connection (service account should have only read/write DNS permisions)
ENV GOOGLE_APPLICATION_CREDENTIALS "credentials.json"

# Command to run script continuously
CMD ["python3", "main.py"]
