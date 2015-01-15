# -*- coding: utf-8 -*-
from misc import get_color_name, get_single_color_definition, need_definition_color


class ConverterGlobals(object):
    def __init__(self):
        self.colors_set = set()

    def get_colors_defines(self):
        need_definition = [(get_color_name(color), get_single_color_definition(color))
                           for color in self.colors_set if need_definition_color(color)]
        return u"".join(u"\\definecolor{%s}%s %%\n" % params for params in need_definition)