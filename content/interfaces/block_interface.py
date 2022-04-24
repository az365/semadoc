from abc import ABC, abstractmethod
from typing import Optional, Iterable, Generator, Any

import type_enums as te

ItemInterface = Any
Native = Any

Title = str


class BlockInterface(ABC):
    @staticmethod
    @abstractmethod
    def from_dict(obj: dict) -> Native:
        pass

    @abstractmethod
    def get_title(self) -> Optional[str]:
        pass

    @abstractmethod
    def set_title(self, title: Title) -> Native:
        pass

    @abstractmethod
    def get_block_type(self) -> te.BlockType:
        pass

    @abstractmethod
    def set_block_type(self, block_type: te.BlockType) -> Native:
        pass

    @abstractmethod
    def get_anchor(self) -> str:
        pass

    @abstractmethod
    def set_anchor(self, anchor: str) -> Native:
        pass

    @abstractmethod
    def get_items(self) -> list:
        pass

    @abstractmethod
    def add_items(self, items: Iterable) -> Native:
        pass

    @abstractmethod
    def append_item(self, item: ItemInterface) -> Native:
        pass

    @abstractmethod
    def merge_block(self, block: Native) -> Native:
        pass

    @abstractmethod
    def get_content_count(self):
        pass

    @abstractmethod
    def get_outgoing_links_iter(self) -> Generator:
        pass

    @abstractmethod
    def get_link_types(self) -> list:
        pass

    @abstractmethod
    def get_links_type(self) -> te.LinkType:
        pass

    @abstractmethod
    def get_text(self):
        pass

    @abstractmethod
    def get_markdown(self):
        pass

    @abstractmethod
    def get_html(self):
        pass
