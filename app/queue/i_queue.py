from abc import ABC, abstractmethod


class IQueue(ABC):

    @abstractmethod
    def disconnect(self):
        """ """

    @abstractmethod
    def create_queue(self, queue_name: str):
        """ """

    @abstractmethod
    def create_exchange(self, exchange: str):
        """ """

    @abstractmethod
    def consume(self, queue_name: str, callback):
        """ """

    @abstractmethod
    def publish(self, exchange: str, routing_key: str, body):
        """ """

    @abstractmethod
    def make_binding(self, exchange: str, queue_name: str):
        """ """

    @abstractmethod
    def start_consuming(self):
        """ """

    @abstractmethod
    def get_channel(self):
        """ """
