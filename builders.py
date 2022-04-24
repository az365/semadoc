try:  # Assume we're a submodule in a package.
    from interfaces import NodeInterface, EdgeInterface, LinkInterface
    import classes as cs
except ImportError:  # Apparently no higher-level package has been imported, fall back to a local import.
    from .interfaces import NodeInterface, EdgeInterface, LinkInterface
    from . import classes as cs


LINK_BLOCKS = ('nodes', 'sources')

ITEM_KEYS_SYNONYMS = (
    ('name', 'id'),
    ('titles', 'title'),
    ('snippets', ),
    ('cats', 'cat', 'parent'),
    ('blocks', 'block', 'content'),
    ('nodes', 'struct', 'list', 'child', 'children'),
    ('sources', 'src', 'source'),
)


def get_node_from_dict_obj(obj: dict, register: bool = True) -> NodeInterface:
    obj = cs.get_standardized_dict(obj, ITEM_KEYS_SYNONYMS)
    node = cs.Node(
        name=obj.pop('name', None),
        titles=obj.pop('titles', None),
        content_blocks=obj.pop('blocks', None),
        link_blocks=obj.pop('name', None),
        register=register,
    )
    for k, v in obj.items():
        node.add_key_value(k, v)
    return node


def get_link_from_dict_obj(obj: dict, register: bool = True) -> LinkInterface:
    obj = cs.get_standardized_dict(obj, ITEM_KEYS_SYNONYMS)
    # <...>


def get_item_from_key_value(key, value):
    pass
