import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

# Logging
import logging
logging.basicConfig(format='%(asctime)s -  %(levelname)s - %(message)s')
logger = logging.getLogger('email')
logger.setLevel(logging.INFO)

def send_email(sender, receiver, subject, body):
    """
    Send an email using the attributes provided
    Args:
        sender (str) : Email ID of sender
        receiver (str) : Email ID of receiver
        subject (str) : Subject of the Email
        body (str) : Email Body
    Returns:
    """
    host = os.getenv('EMAIL_HOST')
    port = os.getenv('EMAIL_PORT')
    username = os.getenv('EMAIL_USERNAME')
    password = os.getenv('EMAIL_PASSWORD')

    # Construct standard email message object
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = subject
    body = body
    msg.attach(MIMEText(body, 'html', 'utf-8'))
    message = msg.as_string()

    logger.info(f"Sending email via {host}:{port}.. ")

    # Send the Email
    try:
        with smtplib.SMTP(str(host), port) as mail_server:
            # TLS for Encryption
            mail_server.starttls()

            # Log into SMTP server
            mail_server.login(username, password)

            # Send the mail
            mail_server.sendmail(sender, receiver, message)
            logger.info(f"Email Sent!")
    except:
        logging.exception("Error")

