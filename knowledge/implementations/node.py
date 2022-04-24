from typing import Optional, Iterable, Generator, Union, Any, NoReturn

try:  # Assume we're a submodule in a package.
    from utils import get_canonic_synonym
    from interfaces import GraphInterface, NodeInterface, EdgeInterface, LinkInterface, BlockInterface
    import type_enums as te
    import classes as cs
    import builders as bs
except ImportError:  # Apparently no higher-level package has been imported, fall back to a local import.
    from ...utils import get_canonic_synonym
    from ...interfaces import GraphInterface, NodeInterface, EdgeInterface, LinkInterface, BlockInterface
    from ... import type_enums as te
    from ... import classes as cs
    from ... import builders as bs

Native = NodeInterface
Name = str
Title = str
Caption = str
Key = str  # Union[str, LinkType, BlockType]
Primitive = Union[str, int, float, bool]

PRIMITIVE_TYPES = str, int, float, bool
ARRAY_TYPES = list, tuple

NODE_KEYS_SYNONYMS = (
    ('name', 'id'),
    ('titles', 'title',),
    ('type', ),
    ('blocks', ),
    ('items', 'node', 'node', 'nodes', 'content', 'list', 'struct'),
    ('links', 'link'),
)
IGNORE_KEYS = 'snippet', 'properties', 'url', 'author', 'year', 'org'
KEYS_PRIMITIVE = 'title', 'info'


class Node(NodeInterface):
    def __init__(
            self,
            name: Name = None,
            titles: Optional[list] = None,
            content_blocks: Optional[list] = None,
            link_blocks: Optional[dict] = None,
            register: bool = True,
    ):
        self._name = name
        self._titles = titles or list()
        self._content_blocks = content_blocks or list()
        self._link_blocks = link_blocks or dict()
        if register:
            self.register()

    def __eq__(self, other: NodeInterface) -> bool:
        if other is None:
            return False
        else:
            return self.get_name() == cs.get_name(other)

    @staticmethod
    def build_node_from_dict(obj: dict, register: bool = True, allow_merge: bool = True) -> NodeInterface:
        name = obj.get('id') or obj.get('name') or obj.get('title')
        node = Node(name=name, register=False)
        node.add_from_dict(obj)
        if register:
            return node.register(allow_merge=allow_merge)
        else:
            return node

    def add_from_dict(self, obj: dict) -> Native:
        for k, v in obj.items():
            self.add_key_value(k, v)
        return self

    @staticmethod
    def get_graph() -> GraphInterface:
        return cs.get_graph()

    def is_registered(self) -> bool:
        return self.get_graph().has_node(self)

    def register(self, allow_merge: bool = True) -> Native:
        print('Adding node {} for {}...         '.format(self.get_name(), str(self.get_graph())[:50]), end='\r')
        node_name = self.get_name()
        if self.get_graph().has_name(node_name):
            if allow_merge:
                return self.get_graph().get_node_by_name(node_name).merge_node(self)
            else:
                raise ValueError('node {} already registered in graph'.format(node_name))
        else:
            self.get_graph().add_node(self)
            return self

    def merge_node(self, node: NodeInterface) -> Native:
        assert self.get_name() == node.get_name()
        for title in node.get_titles():
            self.add_title(title)
        for block in node.get_content_links_iter():
            self.add_content_block(block)
        for link_type, block in node.get_link_blocks_dict().items():
            self.add_link_block(block, link_type=link_type)
        return self

    def get_hash(self):
        return hash(str(self))

    def get_name(self, allow_use_hash: bool = True) -> Name:
        name = self._name
        if not name:
            name = self.get_main_title(allow_use_name=False)
        if allow_use_hash and not name:
            name = str(self.get_hash())
        return name

    def set_name(self, name: Name, allow_rename: bool = False) -> Native:
        old_name = self._name
        if old_name and old_name != name and self.is_registered():
            if allow_rename:
                self.get_graph().rename_item(self.get_name(), name)
            else:
                raise ValueError('can not change registered id for {}'.format(self))
        self._name = name
        return self

    def get_titles(self) -> list:
        return self._titles

    def get_main_title(self, allow_use_name: bool = True) -> Title:
        titles = self.get_titles()
        if titles:
            return titles[0]
        elif allow_use_name:
            return self.get_name()

    def add_title(self, title: Title) -> Native:
        if title not in self.get_titles():
            self.get_titles().append(title)
        return self

    def add_block(self, block: Union[BlockInterface, dict]) -> Native:
        if isinstance(block, dict):
            block = cs.Block.from_dict(block)
        assert isinstance(block, cs.Block)
        if block.get_block_type() == te.BlockType.Links:
            self.add_link_block(block)
        else:
            self.add_content_block(block)
        return self

    def get_link_blocks_types(self) -> list:
        return sorted(self.get_link_blocks_dict().keys())

    def get_link_blocks_list(self) -> list:
        return [self.get_link_block_by_type(t) for t in self.get_link_blocks_types()]

    def get_link_blocks_dict(self) -> dict:
        return self._link_blocks

    def get_link_block_by_type(
            self,
            link_type: Union[te.LinkType, str],
            create_if_not_exists: bool = False,
            skip_missing: bool = False,
    ) -> Optional[LinkInterface]:
        link_type = cs.LinkType.get_type(link_type)
        if create_if_not_exists and link_type not in self.get_link_blocks_dict():
            self.add_link_block_by_type_and_links(link_type, links=list())
        if skip_missing:
            return self.get_link_blocks_dict().get(link_type)
        else:
            return self.get_link_blocks_dict()[link_type]

    def add_link_block(self, block: BlockInterface, link_type: Optional[te.LinkType] = None) -> Native:
        assert isinstance(block, BlockInterface), 'expected Block, got {}'.format(block)
        assert block.get_block_type() == te.BlockType.Links
        if not link_type:
            link_type = block.get_links_type()
        link_block = self.get_link_block_by_type(link_type, create_if_not_exists=True)
        assert isinstance(link_block, cs.Block)
        link_block.merge_block(block)
        return self

    def build_empty_link_block_by_type(self, link_type: te.LinkType) -> BlockInterface:
        assert isinstance(link_type, te.LinkType)
        block_exists = self.get_link_block_by_type(link_type, create_if_not_exists=False, skip_missing=True)
        assert not block_exists
        link_block = cs.Block(block_type=te.BlockType.Links)
        self._link_blocks[link_type] = link_block
        return link_block

    def add_link_block_by_type_and_links(
            self,
            link_type: Union[te.LinkType, str],
            links: Optional[list],
            title: Optional[str] = None,
    ) -> Native:
        link_type = cs.LinkType.get_type(link_type)
        link_block = self.build_empty_link_block_by_type(link_type)
        link_block.set_anchor(link_type.value)
        link_block.set_title(title)
        link_block.add_items(links)
        return self

    def add_link_block_from_dict(self, obj: dict) -> Native:
        link_type_name = obj.get('type') or obj.get('link_type')
        block_type = te.BlockType.Links
        block_title = obj.get('title')
        link_block = cs.Block(title=block_title, block_type=block_type, anchor=link_type_name)
        link_items = obj.get('items') or obj.get('list') or obj.get('links')
        for i in link_items or list():
            if isinstance(i, str):
                link_obj = cs.Link.build_link_from_nodes(from_node=self, to_node=i, link_type=link_type_name)
            elif isinstance(i, dict):
                link_obj = cs.Link.build_link_from_dict(i, from_node=self, link_type=link_type_name)
                assert isinstance(link_obj, cs.Link)
            else:
                raise TypeError('expected Link, got {}'.format(link_obj))
            link_block.append_item(link_obj)
        self.add_link_block(link_block)
        return self

    def get_content_blocks_list(self) -> list:
        return self._content_blocks

    def get_last_content_block(self) -> Optional[BlockInterface]:
        content_blocks = self.get_content_blocks_list()
        if content_blocks:
            block = content_blocks[-1]
            assert isinstance(block, cs.Block)
            return block

    def add_content_block(self, block: Union[BlockInterface, dict], allow_merge: bool = False) -> Native:
        if isinstance(block, dict):
            block = cs.Block.from_dict(block)
        elif isinstance(block, te.BlockType):
            block = cs.Block(block_type=block)
        assert isinstance(block, cs.Block)
        if block not in self.get_content_blocks_list():
            self.get_content_blocks_list().append(block)
        return self

    def add_key_value(self, key: Key, value: Any) -> Native:
        if isinstance(value, dict):
            if 'type' in value:
                key = value.get('type')
        key = get_canonic_synonym(key, NODE_KEYS_SYNONYMS, skip_missing=True) or key
        if key in IGNORE_KEYS:
            return self
        if isinstance(value, PRIMITIVE_TYPES):
            return self.add_primitive_value(key, value)
        if isinstance(value, list):
            return self.add_list_value(key, value)
        if isinstance(value, dict):
            return self.add_dict_value(key, value)
        else:
            raise TypeError('got {}'.format(value))

    def add_primitive_value(self, key: Key, value: Primitive) -> Native:
        if key == 'name':
            self.set_name(value, allow_rename=False)
        elif key == 'titles':
            self.add_title(value)
        elif te.LinkType.has_type(key):
            self.add_link_by_type_and_target(link_type=key, target=value)
        elif te.BlockType.has_type(key):
            self.add_content_item(block_type=key, content_item=value)
        else:
            raise ValueError('Unknown key "{}" for value {}'.format(key, value))
        return self

    def add_list_value(self, key: Key, value: Iterable) -> Native:
        if key == 'name':
            raise ValueError('only one id (name) for edge {} is allowed, got {}'.format(self.get_name(), value))
        for v in value:
            if isinstance(v, PRIMITIVE_TYPES):
                self.add_primitive_value(key, v)
            elif isinstance(v, dict):
                self.add_dict_value(key, v)
            else:
                raise TypeError('expected dict or Primitive({}), got {}'.format(PRIMITIVE_TYPES, v))
        return self

    def add_dict_value(self, key: Key, value: dict) -> Native:
        key = get_canonic_synonym(key, NODE_KEYS_SYNONYMS, skip_missing=True) or key
        if key in KEYS_PRIMITIVE:
            string = ', '.join(['{}: {}'.format(k, v) for k, v in value.items()])
            return self.add_primitive_value(key, string)
        elif te.LinkType.has_type(key):
            link = cs.Link.build_link_from_dict(value, from_node=self, link_type=key)
            self.add_outgoing_link(link)
        elif key in (te.BlockType.Links, 'links'):
            self.add_link_block_from_dict(value)
        elif te.BlockType.has_type(key):
            block = cs.Block.from_dict(value)
            assert isinstance(block, cs.Block)
            block_type = block.get_block_type()
            if block_type == te.BlockType.Links:
                self.add_link_block(block)
            else:
                self.add_content_block(block)
        else:
            raise ValueError('unsupported key {}'.format(key))
        return self

    def add_content_item(self, content_item, block_type: Union[te.BlockType, str]) -> Native:
        block_type = te.BlockType.get_type(block_type)
        assert isinstance(block_type, te.BlockType)
        last_content_block = self.get_last_content_block()
        if last_content_block:
            is_current_block = block_type == last_content_block.get_block_type()
        else:
            is_current_block = False
        if is_current_block:
            assert isinstance(last_content_block, cs.Block)
            last_content_block.append_item(content_item)
        else:
            new_block = cs.Block(block_type=block_type, items=[content_item])
            self.add_content_block(new_block)
        return self

    def add_outgoing_link(self, link: LinkInterface, register: bool = True) -> Native:
        assert isinstance(link, cs.Link)
        link_type = link.get_type()
        link_block = self.get_link_block_by_type(link_type, create_if_not_exists=True)
        assert isinstance(link_block, cs.Block)
        link_block.append_item(link)
        if register:
            self.get_graph().add_edge(link.get_edge(), if_not_exists=True)
        return self

    def add_link_by_type_and_target(
            self, link_type: Union[te.LinkType, str],
            target: Union[NodeInterface, Name, Title],
            caption: Optional[Caption] = None,
            register: bool = True,
            allow_create_node: bool = True,
    ) -> Native:
        link_type = te.LinkType.get_type(link_type)
        to_node = self.get_graph().get_node(target, create_if_not_exists=allow_create_node)
        link_item = cs.Link.build_link_from_nodes(from_node=self, to_node=to_node, link_type=link_type, caption=caption)
        self.add_outgoing_link(link_item, register=register)
        return self

    # deprecated (used in hierdoc)
    def add_link_by_name(self, name: Name, caption: Caption, link_type: te.LinkType, create_node: bool = False):
        node = cs.get_graph().get_node(name)
        if create_node and not node:
            node = cs.Node(name, [caption])
        link = cs.Link.build_link_from_nodes(from_node=self, to_node=node, link_type=link_type, caption=caption)
        self.add_outgoing_link(link)

    def get_content_links_iter(self) -> Generator:
        for block in self.get_content_blocks_list():
            assert isinstance(block, BlockInterface), 'expected Block, got {}'.format(block)
            yield from block.get_outgoing_links_iter()

    def get_link_block_links_iter(self) -> Generator:
        for link_type, block in self.get_link_blocks_dict().items():
            assert isinstance(block, BlockInterface), 'expected Block, got {}'.format(block)
            yield from block.get_outgoing_links_iter()

    def get_child_links_iter(self) -> Generator:
        for block in self.get_content_blocks_list():
            # if block.get_block_type() == cs.BlockType.Links:
            for link in block.get_outgoing_links_iter():
                if link.get_type() == cs.LinkType.Child:
                    yield link

    def get_all_links_iter(self) -> Generator:
        yield from self.get_content_links_iter()
        yield from self.get_link_block_links_iter()

    def get_link(self, node: NodeInterface, link_type: te.LinkType) -> LinkInterface:
        name = cs.get_name(node)
        for link in self.get_all_links_iter():
            assert isinstance(link, cs.Link)
            if link.get_target_node().get_name() == name and link.get_type() == link_type:
                return link

    def get_outgoing_links_iter(self) -> Generator:
        for block in self.get_content_blocks_list():
            yield from block.get_outgoing_links_iter()
        yield from self.get_all_links_iter()

    def has_outgoing_link_to_node(self, node: NodeInterface) -> bool:
        for link in self.get_all_links_iter():
            assert isinstance(link, cs.Link)
            if link.get_target_node() == node:
                return True
        return False

    def has_outgoing_edge(self, edge: EdgeInterface) -> bool:
        if edge.get_a() == self:
            other = edge.get_b()
        elif edge.get_b() == self:
            other = edge.get_a()
        else:
            other = None
        return other and self.has_outgoing_link_to_node(other)

    def get_incoming_edges(self) -> Iterable:
        return cs.get_graph().get_incoming_edges(self)

    def get_incoming_links(self) -> Iterable:
        for edge in self.get_incoming_edges():
            yield edge.get_other_link(self)

    def is_hidden(self) -> bool:
        return not self.get_content_blocks_list() and not self.get_link_blocks_dict()

    def show(self) -> NoReturn:
        for line in self.get_text():
            print(line)

    def get_text(self) -> Generator:
        yield from ['# {}'.format(t) for t in self.get_titles()]
        yield ''
        for block in self.get_content_blocks_list():
            assert isinstance(block, BlockInterface), 'expected Block, got {}'.format(block)
            yield from block.get_text()
            yield ''
        for link_type, block in self.get_link_blocks_dict().items():
            assert isinstance(block, BlockInterface)
            yield from block.get_text()
            yield ''

    def get_page(self):
        return cs.Page(self)

    def __repr__(self):
        template = 'Node("{}", titles={}, content_blocks={}, link_blocks={})'
        return template.format(
            self.get_name(allow_use_hash=False), self.get_titles(),
            self.get_content_blocks_list(),
            {k.value: [(i.get_source_name(), i.get_target_name()) for i in v.get_items()] for k, v in self.get_link_blocks_dict().items()},
        )
