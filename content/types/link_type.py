from enum import Enum

from utils import get_canonic_synonym, is_in_synonyms
from knowledge.types.edge_type import EdgeType

LINK_TYPE_SYNONYMS = (
    ('parent', 'cat', 'cats'),
    ('child', 'children', 'struct', 'content', 'list', 'items', 'nodes'),
    ('uses', 'use'),
    ('usage', 'usages'),
    ('prereq', 'base'),
    ('more', ),
    ('source', 'src', 'sources'),
    ('receptor', 'dst'),
    ('also', 'see_also'),
    ('relation', ),
    ('reference', ),
    ('mention', ),
)


class LinkType(Enum):
    Parent = 'parent'
    Child = 'child'
    Uses = 'uses'
    Usage = 'usage'
    Prereq = 'prereq'
    More = 'more'
    Source = 'source'
    Receptor = 'receptor'
    Also = 'also'
    Relation = 'relation'
    Reference = 'reference'
    Mention = 'mention'

    def get_edge_type(self):
        for edge_type in EdgeType:
            if self in edge_type.get_link_types():
                return edge_type

    def get_direction(self):
        return self.get_edge_type().get_link_types()[1] == self

    @staticmethod
    def get_type(link_type, skip_missing: bool = False):
        if isinstance(link_type, str):
            link_type = get_canonic_synonym(link_type, synonyms_list=LINK_TYPE_SYNONYMS, class_name='Link')
            return LinkType(link_type)
        elif isinstance(link_type, LinkType):
            return link_type
        elif skip_missing:
            return None
        else:
            raise ValueError('LinkType({}) not exists'.format(link_type))

    @staticmethod
    def has_type(link_type) -> bool:
        if isinstance(link_type, str):
            return is_in_synonyms(link_type, synonyms_list=LINK_TYPE_SYNONYMS)
        elif isinstance(link_type, LinkType):
            return True

    @staticmethod
    def get_default():
        return LinkType.Reference
