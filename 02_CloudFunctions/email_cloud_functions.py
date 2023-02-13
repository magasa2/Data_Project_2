#Import libraries
import json
import smtplib
import ssl
from email.message import EmailMessage

from concurrent.futures import TimeoutError
from google.cloud import pubsub_v1

# Input variables
project_id = "your-project-id"
subscription_name = "your-subscription-id"
# Number of seconds the subscriber should listen for messages
timeout = 5.0
email_sender = 'sender_address' 
email_password = 'sender_password'
email_receiver = 'receiver_address'



#Close PubSub Client
class PubSubMessages:
    #Initialise PubSub Client
    def __init__(self, project_id, subscription_name):
        self.subscriber = pubsub_v1.SubscriberClient()
        self.project_id = project_id
        self.subscription_name = subscription_name

    #Read/Subscribe message from PubSub Topic
    def subscribeMessages(self, message):
        # The `subscription_path` method creates a fully qualified identifier in the form f`projects/{project_id}/subscriptions/{subscription_id}`
        subscription_path = self.subscriber.subscription_path(project_id, subscription_name)
        streaming_pull_future = self.subscriber.subscribe(subscription_path, callback=callback)
        print(f"Listening for messages on {subscription_path}..\n")

    #Close PubSub Client
    def __exit__(self):
        self.subscriber.transport.close()
        print("PubSub Client closed.")

def callback(message: pubsub_v1.subscriber.message.Message) -> None:

    print(f"Received {message}.")
    message.ack()

def sending():
    pubsub_class = PubSubMessages(project_id, subscription_name)
    try:
        while True:
            pubsub_class.subscribeMessages(pubsub_v1.subscriber.message.Message)
            # Write the subject and body of the email to be sent.
            subject = 'Hello'
            body = f"""
            This is an alert!
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
    except Exception as err:
        print("Error while inserting data into PubSub Topic: %s", err)
    finally:
        pubsub_class.__exit__()
    


    

# Executing the code by calling the function        
sending()
