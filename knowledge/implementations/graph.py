from typing import Optional, Generator, Iterable, Union, NoReturn
import gc

try:  # Assume we're a submodule in a package.
    from utils import singleton
    from interfaces import GraphInterface, NodeInterface, EdgeInterface, LinkInterface, BlockInterface
    import type_enums as te
    import classes as cs
    import builders as bs
except ImportError:  # Apparently no higher-level package has been imported, fall back to a local import.
    from ...utils import singleton
    from ...interfaces import GraphInterface, NodeInterface, EdgeInterface, LinkInterface, BlockInterface
    from ... import type_enums as te
    from ... import classes as cs
    from ... import builders as bs

Native = GraphInterface
Name = str
Title = str


@singleton
class Graph(GraphInterface):
    def __init__(
            self,
            nodes: Optional[dict] = None,
            edges: Optional[dict] = None,
    ):
        self._nodes = nodes or dict()
        self._edges = edges or dict()

    def clear(self) -> Native:
        self._nodes.clear()
        self._edges.clear()
        gc.collect()
        return self

    def get_nodes_dict(self) -> dict:
        return self._nodes

    def get_nodes_iter(self) -> Iterable:
        return self.get_nodes_dict().values()

    def get_nodes_list(self) -> list:
        return list(self.get_nodes_iter())

    def get_node_names_list(self) -> list:
        return list(self.get_nodes_dict().keys())

    def get_node_count(self) -> int:
        return len(self.get_nodes_dict())

    def has_name(self, name: str) -> bool:
        return name in self.get_nodes_dict()

    def has_node(self, obj: Union[NodeInterface, Name, Title]) -> bool:
        return self.get_node(obj) is not None

    def get_node(self, obj: Union[NodeInterface, Name, Title], create_if_not_exists: bool = False) -> Optional[NodeInterface]:
        if isinstance(obj, str):
            name = obj
        else:
            name = cs.get_name(obj)
        node = self.get_node_by_name(name)
        if not node:
            node = self.get_node_by_title(name)
        if node:
            assert isinstance(node, NodeInterface), 'got {}'.format(node)
            if isinstance(obj, cs.Node):
                assert node == cs.get_node(obj)
        elif create_if_not_exists:
            if isinstance(obj, cs.Node):
                self.add_node(obj)
                return obj
            elif isinstance(obj, Name):
                node = cs.Node(name=node)
                self.add_node(node)
                return node
            else:
                raise TypeError('expected Node or str, got {}'.format(obj))
        return node

    def get_node_by_name(self, name: Name, default=None) -> Optional[NodeInterface]:
        assert isinstance(name, str)
        if name in self.get_nodes_dict():
            return self.get_nodes_dict()[name]
        return self.get_node_by_title(name, default)

    def get_node_by_title(self, title: Title, default=None) -> Optional[NodeInterface]:
        assert isinstance(title, str)
        for node in self.get_nodes_dict().values():
            assert isinstance(node, NodeInterface), node
            if title in node.get_titles():
                return node
        return default

    def add_node(self, node: NodeInterface) -> Native:
        assert isinstance(node, NodeInterface), 'expected Node, got {}'.format(node)
        name = node.get_name()
        self.get_nodes_dict()[name] = node
        return self

    def rename_item(self, old_name: Name, new_name: Name) -> NoReturn:
        assert isinstance(old_name, str)
        assert isinstance(new_name, str)
        assert old_name in self._nodes
        assert new_name not in self._nodes
        item = self.get_node(old_name)
        self._nodes[new_name] = item
        del self._nodes[old_name]

    def add_edge(self, edge: EdgeInterface, if_not_exists: bool = False) -> Native:
        assert isinstance(edge, cs.Edge)
        name_tuple = edge.get_name_tuple()
        existing_edge = self.get_edge(*name_tuple)
        if existing_edge:
            edge = existing_edge
        else:
            self._edges[name_tuple] = edge
        if edge.get_a().get_name() not in self._nodes:
            assert not edge.get_a().is_registered()
            self.add_node(edge.get_a())
        if edge.get_b().get_name() not in self._nodes:
            assert not edge.get_b().is_registered()
            self.add_node(edge.get_b())
        return self

    def get_edge(self, a_name, b_name, edge_type, default=None):
        assert isinstance(a_name, str)
        assert isinstance(b_name, str)
        assert isinstance(edge_type, (cs.EdgeType, str))
        edge_type_str = edge_type if isinstance(edge_type, str) else edge_type.value
        return self._edges.get((a_name, b_name, edge_type_str), default)

    def get_edges_dict(self):
        return self._edges

    def get_edges_for_node(self, node: Union[NodeInterface, Name]) -> Generator:
        for name_tuple, edge in self.get_edges_dict().items():
            if isinstance(node, cs.Node) and node in edge.get_nodes():
                yield edge
            if isinstance(node, Name) and node in name_tuple:
                yield edge

    def get_edge_count(self) -> int:
        return len(self.get_edges_dict())

    def get_outgoing_edges(self, node: Union[NodeInterface, Name]) -> Iterable:
        for edge in self.get_edges_for_node(node):
            if edge.is_defined_in_item(node):
                yield edge

    def get_incoming_edges(self, node: Union[NodeInterface, Name]) -> Iterable:
        for edge in self.get_edges_for_node(node):
            if not edge.is_defined_in_item(node):
                yield edge

    def drop_edge(self, edge: Union[EdgeInterface, tuple]) -> Native:
        if isinstance(edge, tuple):
            edge_name_tuple = edge
        elif isinstance(edge, cs.Edge):
            edge_name_tuple = edge.get_name_tuple()
        else:
            raise TypeError('got {}'.format(edge))
        assert edge_name_tuple in self.get_edges_dict(), 'edge {} not found'.format(edge_name_tuple)
        self.get_edges_dict().pop(edge_name_tuple)
        return self

    def __repr__(self):
        return 'Graph({} nodes, {} edges)'.format(self.get_node_count(), self.get_edge_count())

    def __str__(self):
        return self.__repr__()
