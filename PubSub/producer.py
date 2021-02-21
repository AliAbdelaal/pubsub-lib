from typing import Callable
from PubSub.broker import BrokerClient

class Producer():

    def __init__(self, backend_client:BrokerClient) -> None:
        """Create a consumer object, that listens to specific topic by the given id

        Parameters
        ----------
        backend_client : BrokerClient
            the backend object to communicate the message broker.
        """
        self.backend = backend_client

    def push_msg(self, value:bytes, key:bytes=None):
        """push a message on the object topic

        Parameters
        ----------
        value : bytes
            the message body
        key : bytes
            An optional key that can be sent with the value, by default None.
        """
        self.backend.push_msg(key=key, value=value)
