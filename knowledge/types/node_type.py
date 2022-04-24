from enum import Enum


class NodeType(Enum):
    Unk = 'unk'
    Term = 'term'
    Doc = 'doc'
    Ext = 'ext'
    Img = 'img'

    @staticmethod
    def get_type(node_type, skip_missing: bool = False):
        if isinstance(node_type, str):
            return NodeType(node_type)
        elif isinstance(node_type, NodeType):
            return node_type
        elif skip_missing:
            return None
        else:
            raise ValueError('NodeType({}) not exists'.format(node_type))
