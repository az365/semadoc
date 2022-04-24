from abc import ABC, abstractmethod


class PageInterface(ABC):
    @abstractmethod
    def get_content_blocks(self):
        pass

    @abstractmethod
    def get_blocks(self):
        pass

    @abstractmethod
    def get_content_count(self):
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
