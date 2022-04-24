from typing import Union

from knowledge.implementations.graph import Graph
from knowledge.implementations.edge import Edge
from knowledge.implementations.node import Node
from content.implementations.link import Link
from content.implementations.block import Block


def get_graph() -> Graph:
    return Graph()


def clear_graph():
    return get_graph().clear()


def get_node(obj: Union[Node, Link, str]) -> Node:
    if isinstance(obj, Node):
        return obj
    elif isinstance(obj, Link):
        return obj.get_source_node()
    elif isinstance(obj, str):
        return get_graph().get_node(obj)
    else:
        raise TypeError('obj-argument must be a name as str or an instance of cs.Item or cs.Link')


def get_name(item) -> str:
    if isinstance(item, str):
        return item
    elif isinstance(item, dict):
        return item.get('name', item.get('id'))
    elif hasattr(item, 'get_name'):
        return item.get_name()
    else:
        raise AttributeError('item {} has no name-attribute'.format(item))


def get_edge(obj) -> Edge:
    if isinstance(obj, Edge):
        return obj
    elif isinstance(obj, Link):
        return obj.edge
    elif isinstance(obj, str):
        return get_graph().get_edge(obj)
    else:
        raise TypeError('obj-argument must be a name as str or an instance of cs.Edge or cs.Link')
