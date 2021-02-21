import os
import json
from time import sleep
from typing import Callable
from threading import Thread
from PubSub.consumer import Consumer
from PubSub.producer import Producer
from PubSub.kafka_client import KafkaClient
from PubSub.gcp_pubsub_client import GooglePubSubClient

def runner():
    while True:
        sleep(.1)


class PubSubFactory():

    def __init__(self, vendor: str) -> None:
        """Create a PubSubFactory instance that you can use to initiate a consumer/producer instnances.

        Parameters
        ----------
        vendor : str
            The vendor to use, either 'kafka' or 'gcp'
        """
        if vendor not in ['gcp', 'kafka']:
            raise ValueError(
                f"Vendor : `{vendor}` is not supported yet, only `kafka` and `gcp` are supported.")
        self.vendor = vendor
        self.configs = json.load(open(os.getenv('PUBSUB_CONFIG_PATH')))

    def create_consumer(self, topic_id: str, callback: Callable):
        """create a consumer object that listen on the given topic and apply
        the callable function.

        Parameters
        ----------
        topic_id : str
            the topic ID to listen to.
        callback : Callable
            The function to apply if a message was received.
        """
        backend = None
        if self.vendor == 'kafka':
            backend = KafkaClient(topic_id, self.configs['kafka_servers'])
            Consumer(backend, callback)
        else:
            project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
            subscription_id = os.getenv("GOOGLE_PUBSUB_SUB_ID")
            backend = GooglePubSubClient(project_id=project_id, topic=topic_id,
                                         subscription_id=subscription_id, gcp_configs=self.configs, callback=callback)
            runner_thread = Thread(target=runner)
            runner_thread.start()

    def create_producer(self, topic_id: str) -> Producer:
        """create a producer object that pushes messages on the given topic.

        Parameters
        ----------
        topic_id : str
            The topic ID to push messages to.

        Returns
        -------
        Producer
            The producer object.
        """
        backend = None
        if self.vendor == 'kafka':
            backend = KafkaClient(topic_id, self.configs['kafka_servers'])
        else:
            project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
            subscription_id = os.getenv("GOOGLE_PUBSUB_SUB_ID")
            backend = GooglePubSubClient(project_id=project_id, topic=topic_id,
                                         subscription_id=subscription_id, gcp_configs=self.configs)

        return Producer(backend)
