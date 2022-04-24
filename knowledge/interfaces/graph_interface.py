from abc import ABC, abstractmethod
from typing import Optional, Iterable, Union, Any, NoReturn

Native = Any
NodeInterface = Any
EdgeInterface = Any
Name = str
Title = str


class GraphInterface(ABC):
    @abstractmethod
    def clear(self):
        pass

    @abstractmethod
    def get_nodes_dict(self) -> dict:
        pass

    @abstractmethod
    def get_nodes_list(self) -> list:
        pass

    @abstractmethod
    def get_node_names_list(self) -> list:
        pass

    @abstractmethod
    def has_name(self, name: str) -> bool:
        pass

    @abstractmethod
    def has_node(self, obj: Union[NodeInterface, Name, Title]) -> bool:
        pass

    @abstractmethod
    def get_node(self, obj: Union[NodeInterface, Name, Title], create_if_not_exists: bool = False):
        pass

    @abstractmethod
    def get_node_by_name(self, name: Name, default=None) -> Optional[NodeInterface]:
        pass

    @abstractmethod
    def get_node_by_title(self, title: Title, default=None) -> Optional[NodeInterface]:
        pass

    @abstractmethod
    def add_node(self, node: NodeInterface) -> Native:
        pass

    @abstractmethod
    def rename_item(self, old_name: Name, new_name: Name) -> NoReturn:
        pass

    @abstractmethod
    def add_edge(self, edge: EdgeInterface, if_not_exists: bool = False):
        pass

    @abstractmethod
    def get_edge(self, a_name, b_name, edge_type, default=None):
        pass

    @abstractmethod
    def get_edges_dict(self):
        pass

    @abstractmethod
    def get_edges_for_node(self, item):
        pass

    @abstractmethod
    def get_outgoing_edges(self, node) -> Iterable:
        pass

    @abstractmethod
    def get_incoming_edges(self, node) -> Iterable:
        pass

    @abstractmethod
    def drop_edge(self, edge) -> Native:
        pass
