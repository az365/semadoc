from enum import Enum
from typing import Union

import type_enums as te


class EdgeType(Enum):
    ParentChild = 'parent_child'
    PrereqMore = 'prereq_more'
    UsesUsage = 'uses_usage'
    SourceReceptor = 'source_receptor'
    AlsoRelation = 'also_relation'
    ReferenceMention = 'reference_mention'

    def get_link_types(self):
        if self == EdgeType.ParentChild:
            return te.LinkType.Parent, te.LinkType.Child
        elif self == EdgeType.PrereqMore:
            return te.LinkType.Prereq, te.LinkType.More
        elif self == EdgeType.UsesUsage:
            return te.LinkType.Uses, te.LinkType.Usage
        elif self == EdgeType.SourceReceptor:
            return te.LinkType.Source, te.LinkType.Receptor
        elif self == EdgeType.AlsoRelation:
            return te.LinkType.Also, te.LinkType.Relation
        elif self == EdgeType.ReferenceMention:
            return te.LinkType.Reference, te.LinkType.Mention

    @staticmethod
    def get_type(edge_type, skip_missing: bool = False):
        if isinstance(edge_type, str):
            return EdgeType(edge_type)
        elif isinstance(edge_type, EdgeType):
            return edge_type
        elif skip_missing:
            return None
        else:
            raise ValueError('EdgeType({}) not exists'.format(edge_type))

    @staticmethod
    def get_default():
        return EdgeType.ReferenceMention
