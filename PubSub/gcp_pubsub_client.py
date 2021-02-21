import os
import json
from typing import Callable, Tuple
from google.auth import jwt
from google.cloud import pubsub_v1

from PubSub.broker import BrokerClient

PUBLISHER_AUDIENCE = "https://pubsub.googleapis.com/google.pubsub.v1.Publisher"
AUDIENCE = "https://pubsub.googleapis.com/google.pubsub.v1.Subscriber"

def ack_msg(func):
    def wrapper(msg):
        func(msg.attributes.get('key', None), msg.data)
        msg.ack()
    return wrapper


class GooglePubSubClient(BrokerClient):
    def __init__(self, project_id: str, topic: str, subscription_id: str, gcp_configs: dict, callback:Callable=None) -> None:
        # auth
        credentials = jwt.Credentials.from_service_account_info(
            gcp_configs, audience=AUDIENCE
        )
        credentials_pub = credentials.with_claims(audience=PUBLISHER_AUDIENCE)

        self.topic_name = f'projects/{project_id}/topics/{topic}'
        self.subscription_path = f'projects/{project_id}/subscriptions/{subscription_id}'
        self.consumer = pubsub_v1.SubscriberClient(credentials=credentials)
        self.producer = pubsub_v1.PublisherClient(credentials=credentials_pub)
        if callback:
            self.consumer.subscribe(self.subscription_path, ack_msg(callback))

    def push_msg(self, value: bytes, key: str = None):
        """Push a message on the topic with the given key and value.

        Parameters
        ----------
        value : bytes
            The value bytes
        key : bytes
            The optional key, by default None
        """
        self.producer.publish(self.topic_name, value, key=key)

    def pull_msg(self) -> Tuple[str, bytes]:
        """A blocking function to get the message.

        Returns
        -------
        Tuple[str, bytes]
            key and value in bytes
        """
        raise NotImplementedError()