from typing import Tuple


class BrokerClient():

    def __init__(self, topic:str, *args, **kwargs) -> None:
        """A broker client that supports message pushing and pulling

        Parameters
        ----------
        topic : str
            The topic ID to push or pull from.
        """
        self.topic = topic
        raise NotImplementedError()

    def push_msg(self, value:bytes, key:str=None):
        """push the given message on the topic

        Parameters
        ----------
        value : bytes
            the mesage body.
        key : str
            the mesage key.
        """
        raise NotImplementedError()

    def pull_msg(self)->Tuple[str, bytes]:
        """pull a message from the stored topic, this is a blocking function.

        Returns
        -------
        Tuple[str, bytes]
            the key str and the value bytes.
        """
        raise NotImplementedError()
