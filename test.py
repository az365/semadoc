try:  # Assume we're a submodule in a package.
    from . import hierdoc as ct
except ImportError:  # Apparently no higher-level package has been imported, fall back to a local import.
    import hierdoc as ct


def test_paragraph():
    test_cases = (
        (ct.Paragraph('    mytext', adjust_level=True), 1, 'mytext', '    mytext'),
        (ct.Paragraph('    mytext', adjust_level=False), 0, '    mytext', '    mytext'),
        (ct.Paragraph('абырвалг', adjust_level=False), 0, 'абырвалг', 'абырвалг'),
    )
    for no, (paragraph, level, text, line) in enumerate(test_cases):
        assert paragraph.level == level, 'test case: {}, property: {}, failed'.format(no, 'level')
        assert paragraph.text == text, 'test case: {}, property: {}, failed'.format(no, 'text')
        assert paragraph.get_line() == line, 'test case: {}, property: {}, failed'.format(no, 'line')
        print(paragraph.get_name())


def test_tree():
    test_cases = (
        ('title\n    - line 1\n        - line 2\n    - line 3', 2, 4, 2),
        ('title\n    - line 1\n        - line 2\n            - line 3\n    - line 4', 2, 5, 3),
    )
    for no, (test_text, subtrees_count, lines_count, depth) in enumerate(test_cases):
        tree = ct.Tree(test_text)
        assert tree.get_subtrees_count() == subtrees_count, 'failed case: {}, property: {}'.format(no, 'subtrees')
        assert tree.get_lines_count() == lines_count, 'failed case: {}, property: {}'.format(no, 'lines')
        assert tree.get_depth() == depth, 'failed case: {}, property: {}'.format(no, 'depth')

        for line in tree.get_markdown():
            print(line)


def tests():
    test_tree()
