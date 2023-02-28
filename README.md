# Overview
Simple Python app working "like" DynamicDNS, checks every 15 minutes current public IP address with IP in provided DNS A record and if they are different updates record to the new one. If record doesn't exist yet you have to use `create` instead of `patch` method from `google-api-python-client` package and change app code in `main.py` a little bit

# Prerequirements
* Docker installed
* Service account JSON credentials generated in GCP with read/write privileges to Cloud DNS API (replace data in `credentials.json` file or change env variable `GOOGLE_APPLICATION_CREDENTIALS` to new file name)

# Environment variables
In Dockerfile you have to change some environment variables to proper ones:
- `GCP_PROJECT_ID`
- `GCP_DNS_ZONE`
- `GCP_A_RECORD`
- `GOOGLE_APPLICATION_CREDENTIALS`

# Deploy
To build docker image:
- `docker build -t gcp-dns-update .`

To run docker container from image:
- `docker run -itd gcp-dns-update`

# GCP Cloud DNS API documentation
https://cloud.google.com/dns/docs/reference/v1/

For record set operations:
https://cloud.google.com/dns/docs/reference/v1/resourceRecordSets/