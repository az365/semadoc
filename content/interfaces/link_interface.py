from abc import ABC, abstractmethod


class LinkInterface(ABC):
    @abstractmethod
    def get_edge(self):
        pass
