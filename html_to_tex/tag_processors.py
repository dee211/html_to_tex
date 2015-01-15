# -*- coding: utf-8 -*-
from copy import copy
from itertools import chain, izip, izip_longest
from constants import empty_mdframed_begin
from helpers import cache_result, max_soft, only_true
from misc import dict_to_string
from processor import AbstractProcessor
from state_storage import StateStorage
from style_storage import StyleStorage
from tree_nodes import LatexTreeVoidNode, LatexTreeExactLeaf, LatexTreeNode, LatexTreeLeaf


class BaseTagProcessor(AbstractProcessor):
    additional_styles = {}
    force_create = False

    def __init__(self, tag, parent, config, globals):
        super(BaseTagProcessor, self).__init__(tag, parent, config, globals)
        self.state = StateStorage(tag, config, globals)
        if parent:
            self.state.add_parent_storage(parent.state)
        self.state.merge_less_priority_styles(self.get_additional_styles())
        self.children = []

    def build(self):
        self.children = self.get_children()
        for child in self.children:
            child.build()

    def get_children(self):
        return []

    def set_parent(self, parent):
        self.parent = parent

    def get_sub_processor(self, tag):
        return self.config.get_tag_processor(tag, self, self.globals)

    @cache_result
    def as_vertex(self):
        result = LatexTreeNode(self.get_begin(), self.get_end(), force_create=self.force_create)
        for child in self.children:
            result = result.add_child(child.as_vertex())
        return result

    @cache_result
    def get_plain_text_length(self):
        return max_soft(child.get_plain_text_length() for child in self.children) or 1

    @cache_result
    def get_max_word_length(self):
        return max_soft(child.get_max_word_length() for child in self.children) or 0

    def get_additional_styles(self):
        return StyleStorage(self._copy_plain_styles((u'background-color', u'text-background-color')), self.config)

    def _copy_plain_styles(self, *instruction):
        result = copy(self.additional_styles)
        styles = self.state.get_styles()
        result.update({where: styles.get(what, []) for what, where in instruction if styles.get(what)})
        return result

    def is_table(self):
        return False

    def is_tbody(self):
        return False

    def is_tr(self):
        return False

    def is_td(self):
        return False

    def is_li(self):
        return False


class TagProcessor(BaseTagProcessor):

    def get_children(self):
        return [self.get_sub_processor(child_tag) for child_tag in self.tag.contents]


class BlockTagProcessor(TagProcessor):
    begin = ur"\begin{mdframed}"
    end = ur"\end{mdframed}"

    def get_additional_styles(self):
        return StyleStorage(self._copy_plain_styles((u'background-color', u'block-background-color')), self.config)

    def get_block_styles(self):
        block_styles = {}
        for single_style, parameters in self.state.get_block_styles().iteritems():
            for parameter in parameters:
                processor_fabric = self.config.block_style_processors[single_style]
                processor = processor_fabric.get_processor(self.tag, parameter, self.config, self.globals)
                block_styles.update(processor.get_extra_params())
        return block_styles

    def build(self):
        super(BlockTagProcessor, self).build()
        block_styles = self.get_block_styles()
        options = u"[{}]".format(dict_to_string(block_styles)) if block_styles else u""
        self.begin = self.begin + options


class TextTagProcessor(TagProcessor):
    def build(self):
        pass

    @cache_result
    def get_plain_text_length(self):
        return len(self.tag)

    @cache_result
    def get_max_word_length(self):
        return max_soft(len(x) for x in self.tag.split(' ')) or 0

    def as_vertex(self):
        return self.state.apply_styles(LatexTreeLeaf(self.tag))


class ATagProcessor(TagProcessor):
    begin = u"\\href{%s}{\\pbox[t]{\\textwidth}{\\underline{"
    end = u"}}}"

    def build(self):
        super(ATagProcessor, self).build()
        src = self.tag.get(u'href', u'')
        self.begin = self.begin % src


class AddStylesTagProcessor(TagProcessor):

    def __init__(self, tag, parent, additional_styles, config, globals):
        self.additional_styles = additional_styles
        super(AddStylesTagProcessor, self).__init__(tag, parent, config, globals)


class NoDisplayTagProcessor(TagProcessor):
    begin = u""
    end = u""

    def as_vertex(self):
        return LatexTreeVoidNode()

    def build(self):
        pass


class ConstantTagProcessor(BaseTagProcessor):
    value = NotImplemented

    def as_vertex(self):
        return LatexTreeExactLeaf(self.value)


class BRTagProcessor(ConstantTagProcessor):
    value = ur"\leavevmode\\"


class AmpersandTagProcessor(ConstantTagProcessor):
    value = ur"&"


class ListTagProcessor(TagProcessor):
    def get_children(self):
        children = [self.get_sub_processor(child_tag) for child_tag in self.tag.contents]
        return [child for child in children if child.is_li()]


class UlTagProcessor(ListTagProcessor):
    label_parameter = {
        u'disk': ur'\textbullet',
        u'circle': ur'$\circ$',
        u'square': ur'$\square$',
    }
    begin = ur"\begin{itemize}%s"
    end = ur"\end{itemize}"
    force_create = True

    def get_extra_params(self):
        style = self.state.get_styles()
        list_type = style[u'list-style-type'][0] if style.get(u'list-style-type') else u'not_implemented'
        return u"[label=%s]" % self.label_parameter[list_type] if list_type in self.label_parameter else u""

    def build(self):
        super(UlTagProcessor, self).build()
        self.begin = self.begin % self.get_extra_params()


class OlTagProcessor(ListTagProcessor):
    label_parameter = {
        u'r': ur'\arabic*.',
        u'a': ur'\alph*.',
        u'A': ur'\Alph*.',
        u'i': ur'\roman*.',
        u'I': ur'\Roman*.',
    }
    begin = ur"\begin{enumerate}%s"
    end = ur"\end{enumerate}"

    def get_extra_params(self):
        list_type = self.tag.get(u'type', u'r')
        result = self.label_parameter[list_type] if list_type in self.label_parameter else self.label_parameter[u'r']
        return u"[label=%s]" % result

    def build(self):
        super(OlTagProcessor, self).build()
        self.begin = self.begin % self.get_extra_params()


def get_table_border_width(style):
    result = style.get('table-border', [u"0"])
    result = result[0] if result else u"0"
    return None if result == u"0" else result


def get_table_border(style):
    return style.get(u'table-border', [u'0']) or u'0'


class TableTagProcessor(TagProcessor):
    begin = ur"\begin{longtabu} to \linewidth {%s}"
    end = ur"\end{longtabu}"

    def __init__(self, tag, parent, config, globals):
        super(TableTagProcessor, self).__init__(tag, parent, config, globals)
        self.border_width = int(self.state.get_single_style_value(u'border', u'0'))
        self.hline = ur"\Xhline{%s\arrayrulewidth}" % str(self.border_width) if self.border_width != 0 else u""

    def get_children(self):
        children = super(TableTagProcessor, self).get_children()

        def get_rows(children):
            for child in children:
                if child.is_tr():
                    yield child
                elif child.is_tbody():
                    for row in get_rows(child.get_children()):
                        yield row
        rows = list(get_rows(children))
        for child in rows:
            child.set_parent(self)
        return rows

    def build(self):
        if not self.state.has_parent(u"table"):
            super(TableTagProcessor, self).build()
            self.begin = self.begin % self.get_table_definition() + self.hline

    def normalization(self, word_sizes, text_sizes):
        # прим. способ подбора ширины практичеки от балды, однако не пережимает узкие колонки
        middle_value = sum(word_sizes, 0) / float(max(1, len(word_sizes)))
        return [int((middle_value + word + text) / 3) for word, text in izip(word_sizes, text_sizes)]

    def column_data(self, sizes):
        columns_sizes = [max(chain([1], column)) for column in izip(*sizes)]
        summary = float(sum(columns_sizes))
        return [int(1000 * size / summary) for size in columns_sizes]

    def get_table_definition(self):
        cell_sizes = self.cell_map(lambda x: x.get_max_word_length())
        text_lengths = self.cell_map(lambda x: x.get_plain_text_length())
        relative_word_column_sizes = self.column_data(cell_sizes)
        relative_plain_text_sizes = self.column_data(text_lengths)
        columns_sizes = self.normalization(relative_word_column_sizes, relative_plain_text_sizes)
        border = ur"|[%s\arrayrulewidth]" % str(self.border_width) if self.border_width else u""
        inside = border.join(u"X[%s, l]" % str(size) for size in columns_sizes)
        result = u"{border}{inside}{border}".format(inside=inside, border=border)
        return result

    def cell_map(self, callable):
        return [[callable(cell) for cell in row.children if cell.is_td()] for row in self.children]

    def is_table(self):
        return True


class TBodyTagProcessor(TagProcessor):

    def get_children(self):
        children = super(TBodyTagProcessor, self).get_children()
        return [child for child in children if child.is_tr()]

    def is_tbody(self):
        return True


class TrTagProcessor(TagProcessor):
    force_create = True
    begin = u""
    end_template = ur"\\{}%"

    def get_children(self):
        children = super(TrTagProcessor, self).get_children()
        cells = [child for child in children if child.is_td()]
        delimiters = [AmpersandTagProcessor(u"&", self.parent, self.config, self.globals)] * (len(cells) - 1)
        return list(only_true(chain(*izip_longest(cells, delimiters))))

    def get_end(self):
        return self.end_template.format(self.parent.hline)

    def is_tr(self):
        return True


class TdTagProcessor(TagProcessor):
    force_create = True
    begin = ur"\parbox[t]{\linewidth}{"
    end = ur"}"

    def is_td(self):
        return True


class ThTagProcessor(TdTagProcessor):
    additional_styles = {
        u'text-decoration': [u'bold']
    }


class LiTagProcessor(TagProcessor):
    force_create = True
    begin = ur"\item" + empty_mdframed_begin + u"]"
    end = ur"\end{mdframed}"

    def is_li(self):
        return True


class FixedWrapperTagProcessor(TagProcessor):
    def __init__(self, tag, parent, config, globals, begin=u"", end=u""):
        super(FixedWrapperTagProcessor, self).__init__(tag, parent, config, globals)
        self.begin = begin
        self.end = end


class DivTagProcessor(BlockTagProcessor):
    begin = ur"\begin{divmdframed}"
    end = ur"\end{divmdframed}"


class SafePTagProcessor(TagProcessor):
    begin = ur"\leavevmode\\ \phantom{a} \leavevmode\\"
    end = u""


class PTagProcessor(BlockTagProcessor):
    begin = ur"\begin{pmdframed}"
    end = ur"\end{pmdframed}"
