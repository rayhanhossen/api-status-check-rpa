import json
import logging
import warnings
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
for endpoint_key, endpoint_value in api_endpoints.items():
    for data in endpoint_value:
        try:
            # Disable the InsecureRequestWarning
            warnings.filterwarnings('ignore', message='Unverified HTTPS request')

            # Send a GET request to the API endpoint
            response = requests.get(data['apiURL'], verify=False)

            # Check the response status code
            if response.status_code == 200:
                print(f"{endpoint_key} {data['moduleName']} module api - {data['apiURL']} is live.")
                # If the API is live, log the result
                logging.info(f"{endpoint_key} {data['moduleName']} module api - {data['apiURL']} is live.")
        except Exception as e:
            print(f"{endpoint_key} {data['moduleName']} module is currently down. Error - {e}")
            # If the API is down, log the result and send an email notification
            logging.error(f"{endpoint_key} {data['moduleName']} module is currently down. Error - {e}")

            # send Down mail
            subject = f"{endpoint_key} {data['moduleName']} module api is currently down - Urgent attention required"
            body = f"""
                <html>
                    <body>
                        <p style="color: black; font-size: 15px;"><b>Dear Concern,</b></p>
                        <p style="color: black; font-size: 14px;">
                            I am writing to inform you that the {endpoint_key} website, which is powered by the {data['moduleName']} module, is currently down. The API for the website can be found at <a href="{data['apiURL']}">{data['apiURL']}</a>.<br><br>
    
                            As you know, this website plays a vital role in our operations, and we rely on it to provide our clients with important information. The sudden outage has disrupted our workflow and is causing inconvenience to our customers.<br><br>
    
                            We urgently need your attention to investigate and resolve this issue as soon as possible. Please let us know the status of the situation and the steps being taken to rectify it.<br><br>
    
                            If you require any further information from our end to help with the investigation, please let us know, and we will be happy to provide it.<br><br>
    
                            Thank you for your prompt attention to this matter.<br><br>
    
                            Best regards,<br>
    
                            Neutrix Bot
                        </p>
                    </body>
                </html>
                """
            mail_ins.send_mail(subject=subject, body=body)
