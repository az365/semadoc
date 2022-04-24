from typing import Optional, NoReturn

try:  # Assume we're a submodule in a package.
    from interfaces import GraphInterface, NodeInterface, EdgeInterface, LinkInterface, BlockInterface
    import type_enums as te
    import classes as cs
    import builders as bs
except ImportError:  # Apparently no higher-level package has been imported, fall back to a local import.
    from ...interfaces import GraphInterface, NodeInterface, EdgeInterface, LinkInterface, BlockInterface
    from ... import type_enums as te
    from ... import classes as cs
    from ... import builders as bs


class Edge(EdgeInterface):
    def __init__(
            self,
            node_a: NodeInterface,
            node_b: NodeInterface,
            edge_type: te.EdgeType,
            register: bool = True,
    ):
        assert isinstance(node_a, cs.Node), 'got {}'.format(node_a)
        self._node_a = node_a
        assert isinstance(node_b, cs.Node), 'got {}'.format(node_b)
        self._node_b = node_b
        assert isinstance(edge_type, cs.EdgeType), 'got {}'.format(edge_type)
        self._edge_type = edge_type
        if register:
            self.register()

    def get_a(self) -> NodeInterface:
        return self._node_a

    def get_b(self) -> NodeInterface:
        return self._node_b

    def get_nodes(self):
        return self.get_a(), self.get_b()

    def get_node_pairs(self):
        return self.get_nodes(), reversed(self.get_nodes())

    @staticmethod
    def get_graph() -> GraphInterface:
        return cs.get_graph()

    def copy(self):
        return Edge(self._node_a, self._node_b, self._edge_type, register=False)

    def register(self):
        self.get_graph().add_edge(self)

    def get_other_node(self, node: NodeInterface) -> Optional[NodeInterface]:
        name = cs.get_name(node)
        for node, other in self.get_node_pairs():
            if node.get_name() == name:
                return other

    def get_links(self):
        for item, other in self.get_node_pairs():
            yield item.get_link(other, self._edge_type)

    def get_link_pairs(self):
        return list(self.get_links()), reversed(list(self.get_links()))

    def get_other_link(self, item_or_link):
        for link, other in self.get_link_pairs():
            if link == cs.get_link(item_or_link):
                return other

    def get_link_types(self):
        return self._edge_type.get_link_types()

    def get_type(self):
        return self._edge_type

    def get_name_tuple(self):
        return self._node_a.get_name(), self._node_b.get_name(), self.get_type().value

    def is_defined_in_item(self, item):
        return cs.get_graph().get_node(item).has_outgoing_edge(self)

    def is_defined_in_a(self):
        return self._node_a.has_outgoing_link_to_node(self._node_b)

    def is_defined_in_b(self):
        return self._node_b.has_outgoing_link_to_node(self._node_a)

    def drop(self) -> NoReturn:
        self.get_graph().drop_edge(self)
