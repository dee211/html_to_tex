# -*- coding: utf-8 -*-
from misc import get_color_name
from processor import AbstractProcessor
from tree_nodes import LatexTreeNode


class BaseStyleProcessor(AbstractProcessor):

    def as_vertex(self):
        begin = self.get_begin()
        end = self.get_end()
        return LatexTreeNode(begin, end)


class SingleCommandStyleProcessor(object):

    def get_end(self):
        return u"}"


class AbstractBlockStyleProcessor(BaseStyleProcessor):
    def get_extra_params(self):
        pass

    def as_vertex(self):
        return None


class FixedStyleProcessor(BaseStyleProcessor):
    def __init__(self, tag, parameter, config, globals, rules):
        super(FixedStyleProcessor, self).__init__(tag, parameter, config, globals)
        self.rules = rules
        self.begin = self.get_rule(0)
        self.end = self.get_rule(1)

    def get_rule(self, index):
        return self.rules.get(self.parameter, self.rules.get(u"any", (None, None)))[index]


class ColorStyleProcessor(BaseStyleProcessor):
    end = u"}"

    def __init__(self, tag, parameter, config, globals):
        super(ColorStyleProcessor, self).__init__(tag, parameter, config, globals)
        self.globals.colors_set.add(parameter)
        self.color_name = get_color_name(self.parameter)

    def get_begin(self):
        return ur"\textcolor{%s}{" % self.color_name


class BackgroundColorBlockStyleProcessor(AbstractBlockStyleProcessor):
    def get_extra_params(self):
        self.globals.colors_set.add(self.parameter)
        return {
            "backgroundcolor": get_color_name(self.parameter)
        }


class FontSizeStyleProcessor(BaseStyleProcessor):
    end = u"}"

    def get_begin(self):
        return ur"{\fontsize{%s}{%s}\selectfont" % (self.parameter, self.parameter)


class BackgroundColorTextStyleProcessor(BaseStyleProcessor):
    end = u"}"

    def __init__(self, tag, parameter, config, globals):
        super(BackgroundColorTextStyleProcessor, self).__init__(tag, parameter, config, globals)
        self.globals.colors_set.add(parameter)
        self.color_name = get_color_name(self.parameter)

    def get_begin(self):
        return ur"\colorbox{%s}{" % self.color_name


class BlockStyleProcessor(AbstractBlockStyleProcessor):
    def __init__(self, tag, parameter, config, parameter_name, globals):
        super(BlockStyleProcessor, self).__init__(tag, parameter, config, globals)
        self.parameter_name = parameter_name

    def get_extra_params(self):
        return {self.parameter_name: self.parameter}
