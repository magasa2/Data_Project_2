#Import libraries
import base64
import json
import logging
import smtplib
import ssl
from email.message import EmailMessage

# Input variables
email_sender = '<EMAIL>' 
email_password = '<PASSWORD>'
email_receiver = '<EMAIL>'

#Read from PubSub (decode from Base64) & load as json
def pubsub_to_email(event, context):
    logging.getLogger().setLevel(logging.INFO)
    pubsub_message = base64.b64decode(event['data']).decode('utf-8')
    message = json.loads(pubsub_message)


    if "red" in message["status"]:
        subject = f'ALERT: {message["status"]}'
        body = f"""
        To whom it may concern, 

        {message["notification"]}
        Further steps may need to be taken.

        Regards, 
        COMPANY SUGAR
        """
        em = EmailMessage()
        em['From'] = email_sender
        em['To'] = email_receiver
        em['Subject'] = subject
        em.set_content(body)

    elif "yellow" in message["status"]:
        subject = f'WARNING: {message["status"]}'
        body = f"""
        To whom it may concern, 

        {message["notification"]}
        Please check the machine immediately.

        Regards, 
        COMPANY SUGAR
        """
        em = EmailMessage()
        em['From'] = email_sender
        em['To'] = email_receiver
        em['Subject'] = subject
        em.set_content(body)
    
    # Add the SSL layer in order to secure the email. Its encryption scrambles the message making it impossible to read for anyone that tries to intercept it.
    context = ssl.create_default_context()
    
    # Log into the Gmail account send the message using previously set variables.
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())