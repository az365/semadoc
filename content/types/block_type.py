from enum import Enum
from typing import Iterable

from utils import get_canonic_synonym, is_in_synonyms

BLOCK_TYPE_SYNONYMS = (
    ('title', 'head', 'header',),
    ('info', 'text'),
    ('props', 'properties'),
    ('image', 'img'),
    ('links', 'link'),
)


class BlockType(Enum):
    Title = 'title'
    Struct = 'struct'
    Info = 'info'
    Props = 'props'
    Image = 'image'
    Links = 'links'

    @staticmethod
    def get_type_synonyms() -> Iterable[tuple]:
        return BLOCK_TYPE_SYNONYMS

    @classmethod
    def get_type(cls, block_type, skip_missing: bool = False):
        if isinstance(block_type, str):
            block_type = get_canonic_synonym(block_type, synonyms_list=cls.get_type_synonyms(), class_name='Block')
            return BlockType(block_type)
        elif isinstance(block_type, BlockType):
            return block_type
        elif skip_missing:
            return None
        else:
            raise ValueError('BlockType({}) not exists'.format(block_type))

    @classmethod
    def has_type(cls, block_type) -> bool:
        if isinstance(block_type, str):
            return is_in_synonyms(block_type, synonyms_list=cls.get_type_synonyms())
        elif isinstance(block_type, BlockType):
            return True
