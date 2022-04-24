from typing import Optional, Generator, Iterable, Union

try:  # Assume we're a submodule in a package.
    from utils import get_canonic_synonym
    from interfaces import NodeInterface, BlockInterface, LinkInterface
    import type_enums as te
    import classes as cs
except ImportError:  # Apparently no higher-level package has been imported, fall back to a local import.
    from ...utils import get_canonic_synonym
    from ...interfaces import NodeInterface, BlockInterface, LinkInterface
    from ... import type_enums as te
    from ... import classes as cs

Title = str
Text = str
ItemInterface = Union[Title, Text, LinkInterface]
Native = BlockInterface
Array = Union[list, tuple]

ARRAY_TYPES = list, tuple

BLOCK_KEYS_SYNONYMS = (
    ('title', 'caption'),
    ('type', 'block_type'),
    ('items', 'node', 'node', 'nodes', 'content', 'list', 'struct'),
    ('anchor', 'bookmark'),
)


class Block(BlockInterface):
    def __init__(
            self,
            title: Optional[str] = None,
            block_type=None,
            items: Optional[list] = None,
            anchor: Optional[str] = None,
    ):
        assert isinstance(title, str) or title is None, 'got {}'.format(title)
        self._title = title
        if isinstance(block_type, str):
            block_type = cs.BlockType(block_type)
        elif not block_type:
            block_type = cs.BlockType.Info
        assert isinstance(block_type, cs.BlockType)
        self._block_type = block_type
        assert isinstance(items, list) or items is None
        self._items = items or list()
        self._anchor = anchor

    @staticmethod
    def from_dict(obj: dict) -> BlockInterface:
        block = Block()
        for k, v in obj.items():
            k = get_canonic_synonym(k, BLOCK_KEYS_SYNONYMS, class_name='Block')
            if k == 'title' and v:
                block.set_title(v)
            if k == 'type' and v:
                block.set_block_type(v)
            if k == 'anchor' and v:
                block.set_anchor(v)
            if k == 'items':
                if isinstance(v, ARRAY_TYPES):
                    block.add_items(v)
                else:
                    block.append_item(v)
        return block

    def get_title(self) -> Optional[str]:
        return self._title

    def set_title(self, title: Title) -> Native:
        self._title = title
        return self

    def get_block_type(self) -> te.BlockType:
        return self._block_type

    def set_block_type(self, block_type: te.BlockType) -> Native:
        self._block_type = block_type
        return self

    def get_anchor(self) -> str:
        return self._anchor

    def set_anchor(self, anchor: str) -> Native:
        self._anchor = anchor
        return self

    def get_items(self) -> list:
        return self._items

    def add_items(self, items: Iterable) -> Native:
        for i in items:
            self.append_item(i)
        return self

    def append_item(self, item: ItemInterface) -> Native:
        if self.get_block_type() in (cs.BlockType.Title, cs.BlockType.Info):
            assert isinstance(item, str)
        elif self.get_block_type() in (cs.BlockType.Struct, cs.BlockType.Links):
            assert isinstance(item, cs.Link)
        self._items.append(item)
        return self

    def merge_block(self, block: BlockInterface) -> Native:
        assert isinstance(block, cs.Block)
        assert block.get_block_type() == self.get_block_type()
        if block.get_title():
            self.set_title(block.get_title())
        if block.get_anchor():
            self.set_anchor(block.get_anchor())
        for item in block.get_items():
            if item not in self.get_items():
                self.append_item(item)
        return self

    def get_content_count(self):
        return len(self.get_items())

    def get_outgoing_links_iter(self) -> Generator:
        for item in self.get_items():
            if isinstance(item, cs.Link):
                yield item

    def get_link_types(self) -> list:
        distinct_link_types = list()
        for link in self.get_outgoing_links_iter():
            assert isinstance(link, cs.Link)
            link_type = link.get_type()
            if link_type not in distinct_link_types:
                distinct_link_types.append(link_type)
        return distinct_link_types

    def get_links_type(self) -> te.LinkType:
        anchor = self.get_anchor()
        if te.LinkType.has_type(anchor):
            return te.LinkType.get_type(anchor)
        else:
            link_types = self.get_link_types()
            if link_types:
                return link_types[0]
            else:
                return te.LinkType.get_default()

    def get_text(self):
        block_title_line = '[{}] '.format(self.get_block_type().value)
        if self.get_anchor():
            block_title_line += '({}) '.format(self.get_anchor())
        if self.get_title():
            block_title_line += self.get_title()
        yield block_title_line
        for item in self.get_items():
            if isinstance(item, (str, dict)):
                yield item
            else:
                assert isinstance(item, (NodeInterface, LinkInterface)), 'got {}'.format(item)
                yield from item.get_text()

    def get_markdown(self):
        raise NotImplemented

    def get_html(self):
        raise NotImplemented

    def __repr__(self):
        return 'Block("{}", type={}, anchor={}, {} items)'.format(
            self.get_title(), self.get_block_type(),
            self.get_anchor(), len(self.get_items()),
        )
