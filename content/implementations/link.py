from typing import Optional, Union

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

Native = LinkInterface
Name = str
Caption = str


class Link(LinkInterface):
    def __init__(
            self,
            edge: EdgeInterface,
            is_from_b: bool,
            caption: Optional[Caption] = None,
            is_external: bool = False,
    ):
        assert isinstance(edge, cs.Edge)
        self._edge = edge
        assert isinstance(is_from_b, bool)
        self._is_from_b = is_from_b
        if isinstance(caption, list):
            caption = ' '.join(caption)
        assert isinstance(caption, Caption) or caption is None, 'expected str, got {}'.format(caption)
        self._caption = caption
        assert isinstance(is_external, bool)
        self._is_external = is_external

    @classmethod
    def build_edge(
            cls,
            from_node: Union[NodeInterface, Name],
            to_node: Union[NodeInterface, Name],
            link_type: te.LinkType,
            register: bool = True,
    ) -> EdgeInterface:
        edge_type = link_type.get_edge_type()
        from_b = link_type.get_direction()
        if from_b:
            item_a, item_b = to_node, from_node
        else:
            item_a, item_b = from_node, to_node
        return cs.Edge(item_a, item_b, edge_type, register=register)

    @classmethod
    def build_link_from_nodes(
            cls,
            from_node: Union[NodeInterface, Name],
            to_node: Union[NodeInterface, Name],
            link_type: Union[te.LinkType, str],
            caption: Optional[Caption] = None,
            is_external: bool = False,
            create_item_if_not_exists=False,
    ) -> LinkInterface:
        assert to_node, (from_node, to_node, link_type, caption)
        link_type = te.LinkType.get_type(link_type)
        from_node = cls.get_graph().get_node(from_node) or from_node
        to_node = cls.get_graph().get_node(to_node) or to_node
        edge = cls.build_edge(from_node, to_node, link_type)
        is_from_b = link_type.get_direction()
        return cs.Link(
            edge=edge,
            is_from_b=is_from_b,
            caption=caption,
            is_external=is_external,
        )

    @classmethod
    def build_link_from_dict(
            cls,
            obj: dict,
            from_node: NodeInterface,
            link_type: Union[te.LinkType, str, None] = None,
            update_nodes: bool = True,
            create_nodes: bool = True,
    ) -> LinkInterface:
        caption = obj.pop('caption', None) or obj.get('title') or obj.get('name') or obj.get('id')
        link_type = obj.pop('type', None) or link_type
        remaining_dict = obj.copy()
        target_name = remaining_dict.pop('id', None) or remaining_dict.pop('name', None) or obj.get('title')
        target_node = cls.get_graph().get_node(target_name)
        target_exists = target_node is not None
        if target_exists:
            assert isinstance(target_node, NodeInterface), 'got {}'.format(target_node)
            has_content = bool(remaining_dict)
            if has_content and update_nodes:
                target_node.add_from_dict(obj)
        elif create_nodes:
            target_node = cs.Node.build_node_from_dict(obj)
        else:
            raise ValueError('node {} not exists (and option create_nodes=False used): {}'.format(target_name, obj))
        return cls.build_link_from_nodes(
            from_node=from_node,
            to_node=target_node,
            link_type=link_type,
            caption=caption,
        )

    @staticmethod
    def get_graph() -> GraphInterface:
        return cs.get_graph()

    def get_edge(self) -> EdgeInterface:
        return self._edge

    def is_from_b(self) -> bool:
        return self._is_from_b

    def get_caption(self) -> Caption:
        return self._caption

    def copy(self) -> LinkInterface:
        return cs.Link(edge=self.get_edge().copy(), is_from_b=self.is_from_b(), caption=self.get_caption())

    def get_source_node(self) -> NodeInterface:
        if self.is_from_b():
            return self.get_edge().get_b()
        else:
            return self.get_edge().get_a()

    def get_target_node(self) -> NodeInterface:
        if self.is_from_b():
            return self.get_edge().get_a()
        else:
            return self.get_edge().get_b()

    def get_source_name(self) -> Name:
        return self.get_source_node().get_name()

    def get_target_name(self) -> Name:
        return self.get_target_node().get_name()

    def get_type(self) -> te.LinkType:
        link_types = self.get_edge().get_link_types()
        if self.is_from_b():
            return link_types[1]
        else:
            return link_types[0]

    def set_type(self, link_type: Union[te.LinkType, Name]) -> Native:
        link_type = te.LinkType.get_type(link_type)
        edge = self.build_edge(self.get_source_node(), self.get_target_node(), link_type, register=True)
        return self.reset_edge(edge)

    def reset_edge(self, edge: EdgeInterface) -> Native:
        self.get_edge().drop()
        self._edge = edge
        return self

    def is_hidden(self) -> bool:
        return self.get_target_node().is_hidden()

    def get_text(self):
        node = self.get_target_node()
        assert isinstance(node, NodeInterface)
        yield '({}) {}'.format(node.get_name(), self.get_caption() if self.get_caption() else node.get_main_title())

    def get_markdown(self):
        raise NotImplemented

    def get_html(self):
        raise NotImplemented
