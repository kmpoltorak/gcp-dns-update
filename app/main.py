import requests
import socket
import logging
import os

from googleapiclient import discovery, errors
from oauth2client.client import GoogleCredentials
from time import sleep

GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID")
GCP_DNS_ZONE = os.getenv("GCP_DNS_ZONE")
GCP_A_RECORD = os.getenv("GCP_A_RECORD")

# Get current gateway IP by using ifconfig.me website
def get_current_ip():
    try:
        url = "http://ifconfig.me"
        response = requests.get(url)
        return response.text
    except:
        logging.error(f"Unable to check current IP using {url}")

# Resolve DNS name and get current IP in DNS
def get_current_dns_ip():
    try:
        return socket.gethostbyname(GCP_A_RECORD[:-1])
    except:
        logging.error(f"Unable to get IP address from DNS name {fqdn}")

# Update DNS record if IP addresses are different
def update_dns_record():
    try:
        current_ip = get_current_ip()
        current_dns_ip = get_current_dns_ip()
        if current_ip != current_dns_ip:
            # Credentials by default from file provided in environment variable GOOGLE_APPLICATION_CREDENTIALS in Dockerfile
            credentials = GoogleCredentials.get_application_default()
            service = discovery.build('dns', 'v1', credentials=credentials)
            dns_record_body = {
            'name': GCP_A_RECORD,
            'rrdatas': [current_ip],
            'ttl': 600,
            'type': 'A',
            'kind': 'dns#resourceRecordSet'
            }
            request = service.resourceRecordSets().patch(project=GCP_PROJECT_ID, managedZone=GCP_DNS_ZONE, name=GCP_A_RECORD, type="A", body=dns_record_body)
            response = request.execute()
            logging.info(f"Record in DNS has been updated: {response}")
    except errors.HttpError as exc:
        logging.error(exc)


if __name__ == "__main__":
    # Turn on logging to file
    logging.basicConfig(filename="log/debug.log",
                        format="%(asctime)s [%(levelname)s] %(message)s",
                        level=logging.INFO)

    # Make check and update every 15 minutes
    while True:
        update_dns_record()
        sleep(900)
