from typing import Optional, Iterable
import yaml

try:  # Assume we're a submodule in a package.
    import classes as cs
except ImportError:  # Apparently no higher-level package has been imported, fall back to a local import.
    from . import classes as cs


DEFAULT_RULES = {
    'max_header_level': 2,
}
SPACE = ' '
INDENT_STEP = 4
MARKERS = ('*', '-', '+', '>', '&', 'i', '=')
SKIP_MARKERS = ('0', 'x')
NAME_DIVIDERS = (':', ' - ')
MAX_WORDS_IN_NAME = 5


def split_lines(text):
    iterable_text = [text] if isinstance(text, str) else text
    for line in iterable_text:
        for subline in line.split('\n'):
            if subline != '':
                yield subline


def str_has_indent(text):
    if len(text) > INDENT_STEP:
        if text.startswith(SPACE * INDENT_STEP):
            return True
    return False


def transliterate(text):
    symbols = (u"абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ",
               u"abvgdeejzijklmnoprstufhzcss_y_euaABVGDEEJZIJKLMNOPRSTUFHZCSS_Y_EUA")
    tr = {ord(a): ord(b) for a, b in zip(*symbols)}
    return text.translate(tr)


class Paragraph(object):
    def __init__(
            self,
            text,
            level=0,
            adjust_level=True,
    ):
        self.text = text
        self.level = level
        if adjust_level:
            self.adjust_level()

    def get_line(self):
        return SPACE * INDENT_STEP * self.level + self.text

    def set_line(self, text):
        self.text = str(text)
        self.adjust_level()

    def has_indent(self):
        return str_has_indent(self.text)

    def adjust_level(self):
        while str_has_indent(self.text):
            self.level += 1
            self.text = self.text[INDENT_STEP:]

    def get_mark(self, standard_only=True):
        if len(self.text) > 2:
            if self.text[1] == SPACE:
                marker = self.text[0]
                if marker in MARKERS or marker in SKIP_MARKERS or not standard_only:
                    return marker

    def get_text_without_marks(self):
        if self.get_mark():
            return self.text[2:]
        else:
            return self.text

    def get_markdown(self, rules=DEFAULT_RULES):
        max_header_level = rules.get('max_header_level')
        if self.level + 1 <= max_header_level:
            markdown_line = '#' * (self.level + 1) + ' ' + self.get_text_without_marks()
        else:
            markdown_line = SPACE * (self.level - max_header_level) * INDENT_STEP + self.text
        return [markdown_line]

    def get_tag(self):
        text = self.get_text_without_marks() + ' '
        if text.startswith('['):
            closed_scope_position = text.find('] ')
            if closed_scope_position > 2:
                tag = text[1: closed_scope_position]
                tag = tag.lower()
                tag.replace(SPACE, '_')
                return tag

    def get_text_without_marks_and_tags(self):
        tag = self.get_tag()
        if tag:
            return self.get_text_without_marks()[len(tag) + 3:]
        else:
            return self.get_text_without_marks()

    def has_name(self):
        text = self.get_text_without_marks_and_tags()
        if (text or SPACE)[0] == '(':
            closed_scope_position = text.find(')')
            if closed_scope_position > 2:
                return text[1: closed_scope_position]
        for divider in NAME_DIVIDERS:
            if divider in text:
                text = text.split(divider)[0]
            if len(text) < 20:
                return text

    def get_name(self):
        text = self.get_text_without_marks_and_tags()
        if (text or SPACE)[0] == '(':
            closed_scope_position = text.find(') ')
            if closed_scope_position > 2:
                text = text[1: closed_scope_position]
        for divider in NAME_DIVIDERS:
            if divider in text:
                text = text.split(divider)[0]
        splitted_text = text.split(SPACE)
        if len(splitted_text) > MAX_WORDS_IN_NAME:
            text = SPACE.join(splitted_text[:MAX_WORDS_IN_NAME])
        text = text.lower()
        text.replace(SPACE, '_')
        text = transliterate(text)
        return text

    def get_content(self):
        text = self.get_text_without_marks_and_tags()
        name = self.has_name()
        if name:
            return text[len(name) + 3:]
        else:
            return text


Native = Paragraph


class Tree(Paragraph):
    def __init__(
            self,
            text,
            level=0,
            name=None,
            subtrees=tuple(),
    ):
        Paragraph.__init__(self, text, level)
        self.name = name
        if subtrees:
            self.subtrees = list(subtrees)
        else:
            self.set_hiertext(text, including_title=True)

    def get_depth(self):
        max_depth = -1
        for subtree in self.subtrees:
            cur_depth = subtree.get_depth()
            if cur_depth > max_depth:
                max_depth = cur_depth
        return max_depth + 1

    def get_last_subtree(self):
        if self.subtrees:
            return self.subtrees[-1]

    def get_last_subtree_level(self):
        last_subtree = self.get_last_subtree()
        if last_subtree:
            return last_subtree.level

    def get_last_level(self):
        last_subtree_level = self.get_last_subtree_level()
        if last_subtree_level is not None:
            return last_subtree_level
        else:
            return self.level

    def get_mark(self, standard_only=True):
        return self.get_title_paragraph().get_mark(standard_only)

    def remove_commented_subtrees(self, markers=SKIP_MARKERS):
        for subtree in self.subtrees:
            if subtree.get_mark() in markers:
                self.subtrees.remove(subtree)
                print('removed:', subtree.get_title_paragraph().text)
            else:
                subtree.remove_commented_subtrees(markers)

    def add_paragraph(self, paragraph):
        last_subtree_level = self.get_last_subtree_level()
        if (last_subtree_level is not None) and (paragraph.level > last_subtree_level):
            last_subtree = self.get_last_subtree()
            last_subtree.add_paragraph(paragraph)
        else:
            new_subtree = Tree(paragraph.text, paragraph.level)
            self.subtrees.append(new_subtree)

    def add_line(self, text, level=0):
        paragraph = Paragraph(text, level)
        self.add_paragraph(paragraph)

    def add_dict_obj(self, obj: dict) -> Native:
        pass

    def add_yaml_text(self, lines: Iterable) -> Native:
        yaml_data = yaml.safe_load(lines)
        for obj in yaml_data:
            assert isinstance(obj, dict)
            self.add_dict_obj(obj)
        return self

    def add_hiertext(self, hiertext, replace_tab=True, skip_commented=True):
        for line in split_lines(hiertext):
            if replace_tab and line.startswith('\t'):
                line = line.replace('\t', SPACE * INDENT_STEP)
            self.add_line(line)
        if skip_commented:
            self.remove_commented_subtrees()

    def set_hiertext(self, hiertext, including_title=False):
        lines = list(split_lines(hiertext))
        if including_title:
            title = lines[0]
            self.text = title
            lines = lines[1:]
        self.subtrees = list()
        self.add_hiertext(lines)

    def get_title_text(self):
        return self.text

    def get_title_paragraph(self) -> Paragraph:
        return Paragraph(self.text, self.level)

    def get_hiertext(self):
        yield self.get_title_paragraph().get_line()
        for subtree in self.subtrees:
            for line in subtree.get_hiertext():
                yield line

    def get_subtrees_count(self):
        return len(self.subtrees)

    def get_lines_count(self):
        lines_count = 1
        for subtree in self.subtrees:
            lines_count += subtree.get_lines_count()
        return lines_count

    def get_paragraphs(self):
        yield self.get_title_paragraph()
        for subtree in self.subtrees:
            for paragraph in subtree.get_paragraphs():
                yield paragraph

    def get_markdown(self, rules=DEFAULT_RULES):
        for paragraph in self.get_paragraphs():
            markdown_lines = paragraph.get_markdown(rules)
            for line in markdown_lines:
                yield line

    @staticmethod
    def get_detected_doctype_by_filename(filename: str, default: Optional[str] = None) -> str:
        extension = filename.split('.')[-1]
        if extension in ('txt', 'yaml'):
            doctype = extension
            return doctype
        elif default:
            return default
        else:
            raise ValueError

    def from_file(self, filename: str, doctype: str = None) -> Native:
        if doctype is None:
            doctype = self.get_detected_doctype_by_filename()
        file_holder = open(filename, 'r', encoding='utf-8')
        if doctype == 'txt':
            self.add_hiertext(file_holder)
        elif doctype == 'yaml':
            self.add_yaml(file_holder)
        else:
            raise ValueError
        file_holder.close()
        return self

    def get_first_level_lines(self):
        for subtree in self.subtrees:
            yield subtree.get_title_paragraph()

    def get_item(self, as_link_from=None, link_type=cs.LinkType.Reference):
        cur = self.get_title_paragraph()
        tag = cur.get_tag()
        name = cur.get_name()
        caption = cur.get_content()
        titles = caption.split(' = ')
        print('Parsing row: [{}] ({}) "{}"'.format(tag, name, caption))
        item = cs.Node(name, titles=titles)
        for subtree in self.subtrees:
            assert isinstance(subtree, Tree)
            p = subtree.get_title_paragraph()
            p_marker = p.get_mark()
            p_tag = p.get_tag()
            p_name = p.get_name()
            p_text = p.get_content()
            print('....p_marker={}, p_tag={}, p_name={}, p_name={}'.format(p_marker, p_tag, p_name, p_text))
            if p_tag in ('parent', 'category', 'cat'):
                item.add_link_by_name(p_name, caption=p_text, link_type=cs.LinkType.Parent)
            elif p_marker == '=' or p_tag in ('child', 'children', 'struct', 'structure'):
                if p_text.endswith(':') or not p_text:  # and subtree.get_depth() > 1:
                    item.add_content_block(cs.Block(p_text, cs.BlockType.Struct))
                    for element in subtree.subtrees:
                        link = element.get_node(as_link_from=item, link_type=cs.LinkType.Child)
                        item.add_content_item(link.copy(), block_type=cs.BlockType.Struct)
                else:
                    link = subtree.get_item(as_link_from=item, link_type=cs.LinkType.Child)
                    item.add_content_item(link.copy(), block_type=cs.BlockType.Struct)
            elif p_tag == 'usage':
                if p_text.endswith(':'):  # and subtree.get_depth() > 1:
                    for element in subtree.subtrees:
                        e_name = element.get_name()
                        e_text = element.get_content()
                        item.add_link_by_name(e_name, e_text, link_type=cs.LinkType.Usage, create_node=True)
                else:
                    item.add_link_by_name(p_name, p_text, link_type=cs.LinkType.Usage, create_node=True)
            else:
                for t in subtree.get_hiertext():
                    item.add_content_item(t, block_type=cs.BlockType.Info)
        if as_link_from:
            link = cs.Link.build_link_from_nodes(as_link_from, item, link_type=link_type, caption=caption)
            return link
        else:
            return item

# class Page(object):
#     # <...>
#     pass
