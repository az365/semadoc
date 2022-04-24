try:  # Assume we're a submodule in a package.
    import classes as cs
except ImportError:  # Apparently no higher-level package has been imported, fall back to a local import.
    from .. import classes as cs


def test_create_item():
    cs.Node('a')
    assert 'a' in cs.get_graph().items
    assert 'b' not in cs.get_graph().items
    cs.get_graph().clear()


def test_create_edge():
    cs.get_graph().clear()
    b = cs.Node('b')
    c = cs.Node('c')
    cs.Edge(c, b, cs.EdgeType.UsesUsage)
    assert cs.get_graph().get_edge('c', 'b', cs.EdgeType.UsesUsage)
    assert not cs.get_graph().get_edge('b', 'c', cs.EdgeType.UsesUsage)


if __name__ == '__main__':
    test_create_item()
    test_create_edge()
