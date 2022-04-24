from abc import ABC, abstractmethod
from typing import Optional, Iterable, Generator, Union, Any

try:  # Assume we're a submodule in a package.
    import type_enums as te
except ImportError:  # Apparently no higher-level package has been imported, fall back to a local import.
    from ... import type_enums as te

Native = Any
GraphInterface = Any
EdgeInterface = Any
LinkInterface = Any
BlockInterface = Any
PageInterface = Any

Name = str
Title = str
Caption = str


class NodeInterface(ABC):
    @staticmethod
    @abstractmethod
    def get_graph() -> GraphInterface:
        pass

    @abstractmethod
    def register(self) -> Native:
        pass

    @abstractmethod
    def is_registered(self) -> bool:
        pass

    @abstractmethod
    def get_hash(self):
        pass

    @abstractmethod
    def get_name(self) -> Name:
        pass

    @abstractmethod
    def set_name(self, name: Name) -> Native:
        pass

    @abstractmethod
    def get_titles(self) -> list:
        pass

    @abstractmethod
    def get_main_title(self) -> Title:
        pass

    @abstractmethod
    def add_title(self, title: Title) -> Native:
        pass

    @abstractmethod
    def get_link_blocks_types(self) -> list:
        pass

    @abstractmethod
    def get_link_blocks_list(self) -> list:
        pass

    @abstractmethod
    def get_link_blocks_dict(self) -> dict:
        pass

    @abstractmethod
    def get_link_block_by_type(
            self, link_type: Union[te.LinkType, str],
            create_if_not_exists: bool, skip_missing: bool = False,
    ) -> Optional[LinkInterface]:
        pass

    @abstractmethod
    def add_link_block(self, block: BlockInterface, link_type: Optional[te.LinkType] = None) -> Native:
        pass

    @abstractmethod
    def add_link_block_by_type_and_links(
            self, link_type: Union[te.LinkType, str],
            links: Optional[list], title: Optional[str] = None,
    ) -> Native:
        pass

    @abstractmethod
    def get_content_blocks_list(self) -> list:
        pass

    @abstractmethod
    def get_last_content_block(self) -> Optional[BlockInterface]:
        pass

    @abstractmethod
    def add_content_block(self, block: Union[BlockInterface, dict]) -> Native:
        pass

    @abstractmethod
    def add_key_value(self, key: str, value: Any) -> Native:
        pass

    @abstractmethod
    def add_primitive_value(self, key: str, value) -> Native:
        pass

    @abstractmethod
    def add_list_value(self, key: str, value: Iterable) -> Native:
        pass

    @abstractmethod
    def add_dict_value(self, key: str, value: dict) -> Native:
        pass

    @abstractmethod
    def add_content_item(self, content_item, block_type: Union[te.BlockType, str]) -> Native:
        pass

    @abstractmethod
    def add_outgoing_link(self, link: LinkInterface, register: bool = True) -> Native:
        pass

    @abstractmethod
    def add_link_by_type_and_target(
            self, link_type: Union[te.LinkType, str],
            target: Union[Native, Name, Title],
            caption: Optional[Caption] = None,
            register: bool = True,
    ) -> Native:
        pass

    @abstractmethod
    def get_content_links_iter(self) -> Generator:
        pass

    @abstractmethod
    def get_link_block_links_iter(self) -> Generator:
        pass

    @abstractmethod
    def get_child_links_iter(self) -> Generator:
        pass

    @abstractmethod
    def get_all_links_iter(self) -> Generator:
        pass

    @abstractmethod
    def get_link(self, node: Native, link_type: te.LinkType) -> LinkInterface:
        pass

    @abstractmethod
    def get_outgoing_links_iter(self) -> Generator:
        pass

    @abstractmethod
    def has_outgoing_link_to_node(self, node: Native) -> bool:
        pass

    @abstractmethod
    def has_outgoing_edge(self, edge: EdgeInterface) -> bool:
        pass

    @abstractmethod
    def get_incoming_edges(self) -> Iterable:
        pass

    @abstractmethod
    def get_incoming_links(self) -> Iterable:
        pass

    @abstractmethod
    def is_hidden(self) -> bool:
        pass

    @abstractmethod
    def get_text(self) -> Iterable:
        pass

    @abstractmethod
    def get_page(self) -> PageInterface:
        pass
