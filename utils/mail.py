import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from dotenv import load_dotenv

load_dotenv()


class MailSender:

    def send_mail(self, subject, body):
        # Set up the email message
        msg = MIMEMultipart()
        msg['From'] = os.environ.get("FROM_MAIL")
        msg['To'] = os.environ.get("TO_MAIL")
        msg['Cc'] = os.environ.get("CC_MAIL")
        msg['Subject'] = subject

        # Add the message body
        msg.attach(MIMEText(body, 'html'))

        # Set up the SMTP server and send the message
        smtp_server = os.environ.get("EMAIL_HOST")  # Replace with your SMTP server
        smtp_port = os.environ.get("EMAIL_PORT")  # Replace with your SMTP port
        smtp_username = os.environ.get("EMAIL_USER")  # Replace with your SMTP username
        smtp_password = os.environ.get("EMAIL_PASS")  # Replace with your SMTP password

        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            # server.starttls()
            server.login(smtp_username, smtp_password)
            server.sendmail(msg['From'], [msg['To'], msg['Cc']], msg.as_string())

        print('Email sent successfully!')
