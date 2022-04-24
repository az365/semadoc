try:  # Assume we're a submodule in a package.
    from interfaces import GraphInterface, NodeInterface, EdgeInterface, LinkInterface, BlockInterface, PageInterface
    import type_enums as te
    import classes as cs
    import builders as bs
except ImportError:  # Apparently no higher-level package has been imported, fall back to a local import.
    from ...interfaces import GraphInterface, NodeInterface, EdgeInterface, LinkInterface, BlockInterface, PageInterface
    from ... import type_enums as te
    from ... import classes as cs
    from ... import builders as bs


class Page(PageInterface):
    def __init__(
            self,
            item,
    ):
        assert isinstance(item, cs.Node)
        self.item = item

    def get_navig_block(self):
        raise NotImplemented

    def get_title_block(self):
        raise NotImplemented

    def get_content_blocks(self):
        return self.item.get_content_blocks_list()

    def get_links_block(self):
        raise NotImplemented

    def get_blocks(self):
        yield self.get_navig_block()
        yield self.get_title_block()
        yield self.get_content_blocks()
        yield self.get_links_block()

    def get_content_count(self):
        cnt = 0
        for block in self.get_blocks():
            cnt += block.get_content_count()
        return cnt

    def get_text(self):
        for block in self.get_blocks():
            assert isinstance(block, cs.Block)
            yield from block.get_text()

    def get_markdown(self):
        for block in self.get_blocks():
            assert isinstance(block, cs.Block)
            yield from block.get_markdown()

    def get_html(self):
        for block in self.get_blocks():
            assert isinstance(block, cs.Block)
            yield from block.get_html()
