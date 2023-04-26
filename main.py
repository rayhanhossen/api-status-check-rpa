import json
import logging
from datetime import datetime

import requests

from utils.mail import MailSender

# instance of mail sender
mail_ins = MailSender()

# Set up logging
logging.basicConfig(filename=f'./logs/app_{datetime.now().strftime("%d_%m_%Y")}.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s')

# Read API endpoints from JSON file
with open('./public_api_endpoints.json', 'r') as f:
    api_endpoints = json.load(f)

# Loop through each API endpoint
for endpoint_name, endpoint_url in api_endpoints.items():
    try:
        # Send a GET request to the API endpoint
        response = requests.get(endpoint_url)

        # Check the response status code
        if response.status_code == 200:
            # If the API is live, log the result
            logging.info(f'The API at {endpoint_url} is live.')
        else:
            # If the API is down, log the result and send an email notification
            logging.error(f'The API at {endpoint_url} is down with status code {response.status_code}.')

            # send Down mail
            subject = f'API DOWN: {endpoint_name}'
            body = f'The API at {endpoint_url} is down with status code {response.status_code}.'
            mail_ins.send_mail(subject=subject, body=body)
    except Exception as e:
        # If there is an exception, log the error and send an email notification
        logging.error(f'An error occurred while checking the API at {endpoint_url}: {e}')

        # Create the email message
        subject = f'API ERROR: {endpoint_name}'
        body = f'An error occurred while checking the API at {endpoint_url}: {e}'
        mail_ins.send_mail(subject=subject, body=body)
