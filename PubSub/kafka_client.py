from time import sleep
from typing import Tuple, Union
from kafka import KafkaConsumer, KafkaProducer
from PubSub.broker import BrokerClient


class KafkaClient(BrokerClient):

    def __init__(self, topic: str, kafka_servers: Union[str, list], ) -> None:
        """Initiate a Kafka client.

        Parameters
        ----------
        topic : str
            The topic to pub/sub with.
        kafka_server : str
            Kafka server uri.
        """
        self.topic = topic
        self.consumer = KafkaConsumer(topic, bootstrap_servers=kafka_servers,
                                      auto_offset_reset='earliest', enable_auto_commit=True,
                                      group_id='consumers')

        self.producer = KafkaProducer(bootstrap_servers=kafka_servers)

    def push_msg(self, value: bytes, key: str = None):
        """Push a message on the topic with the given key and value.

        Parameters
        ----------
        value : bytes
            The value bytes
        key : str
            The optional key, by default None
        """
        self.producer.send(self.topic, key=key, value=value)
        self.producer.flush()

    def pull_msg(self) -> Tuple[str, bytes]:
        """A blocking function to get the message.

        Returns
        -------
        Tuple[str, bytes]
            key and value in bytes
        """
        for msg in self.consumer:
            key = msg.key.decode() if msg.key else None
            return key, msg.value
