from abc import ABC, abstractmethod
from typing import Any

GraphInterface = Any
NodeInterface = Any

Name = str


class EdgeInterface(ABC):
    @abstractmethod
    def get_a(self) -> NodeInterface:
        pass

    @abstractmethod
    def get_b(self) -> NodeInterface:
        pass

    @abstractmethod
    def get_nodes(self) -> tuple:
        pass

    @abstractmethod
    def get_node_pairs(self) -> tuple:
        pass

    @staticmethod
    @abstractmethod
    def get_graph() -> GraphInterface:
        pass

    @abstractmethod
    def copy(self):
        pass

    @abstractmethod
    def register(self):
        pass

    @abstractmethod
    def get_other_node(self, node: NodeInterface) -> NodeInterface:
        pass

    @abstractmethod
    def get_links(self):
        pass

    @abstractmethod
    def get_link_pairs(self):
        pass

    @abstractmethod
    def get_other_link(self, item_or_link):
        pass

    @abstractmethod
    def get_link_types(self):
        pass

    @abstractmethod
    def get_type(self):
        pass

    @abstractmethod
    def get_name_tuple(self):
        pass

    @abstractmethod
    def is_defined_in_item(self, node: NodeInterface):
        pass

    @abstractmethod
    def is_defined_in_a(self):
        pass

    @abstractmethod
    def is_defined_in_b(self):
        pass

    @abstractmethod
    def drop(self):
        pass
