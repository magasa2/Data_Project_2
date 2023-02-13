###EDEM MDA Data Project 2 Group 3
#Inserting data into a PubSub Topic

#Import libraries
import json
import time
import logging
import argparse
from google.cloud import pubsub_v1

#Define input arguments
parser = argparse.ArgumentParser(description=('Aixigo Contracts Dataflow pipeline.'))
parser.add_argument(
                '--project_id',
                required=True,
                help='GCP cloud project name.')
parser.add_argument(
                '--topic_name',
                required=True,
                help='PubSub topic name.')

args, opts = parser.parse_known_args()

class PubSubMessages:
    #Initialise PubSub Client
    def __init__(self, project_id, topic_name):
        self.publisher = pubsub_v1.PublisherClient()
        self.project_id = project_id
        self.topic_name = topic_name

    #Publish message into PubSub Topic
    def publishMessages(self, message):
        json_str = json.dumps(message)
        topic_path = self.publisher.topic_path(self.project_id, self.topic_name)
        publish_future = self.publisher.publish(topic_path, json_str.encode("utf-8"))
        logging.info("A new datapoint with its ID %s has been registered at %s.", message["id"], message["time"])

    #Close PubSub Client
    def __exit__(self):
        self.publisher.transport.close()
        logging.info("PubSub Client closed.")
            
#Load generated data
def loadGeneratedData():
    f = open('sensor_data.json')
    datapoint = json.load(f)
    return datapoint  

#Publish message into the queue every second
def run_generator(project_id, topic_name):
    pubsub_class = PubSubMessages(project_id, topic_name)
    try:
        while True:
            message: dict = loadGeneratedData()
            pubsub_class.publishMessages(message)
            time.sleep(1)
    except Exception as err:
        logging.error("Error while inserting data into PubSub Topic: %s", err)
    finally:
        pubsub_class.__exit__()

#Run generator process (for publishing messages inkl. logging)
if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    run_generator(args.project_id, args.topic_name)