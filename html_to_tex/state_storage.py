# -*- coding: utf-8 -*-
from classes_storage import ClassStorage
from constants import style_sorting_weight
from style_storage import StyleStorage


class StateStorage(object):
    parent_storage = None

    def __init__(self, tag, config, globals):
        self.tag = tag
        self.globals = globals
        self.config = config
        if self.tag.__class__.__name__ in (u"Tag", u'Document'):
            self.classes = ClassStorage(self.classes_to_set(tag.get(u'class', u'')), config)
            self.style = StyleStorage(self.styles_to_dict(tag.get(u'style', u'')), config)
        else:
            self.classes, self.style = ClassStorage(set(), config), StyleStorage(dict(), config)

    def classes_to_set(self, classes):
        return {single for single in classes.split() if single}

    def add_parent_storage(self, parent_storage):
        self.parent_storage = parent_storage
        self.classes.add_parent(parent_storage.classes)
        self.merge_less_priority_styles(self.classes.to_style())
        self.style.merge_parent(parent_storage.style)

    def styles_to_dict(self, styles_string):
        if styles_string is None:
            return {}
        styles_dict = {}
        for single_style in styles_string.split(';'):
            single_style = single_style.strip(u" ").split(':')
            if len(single_style) > 1:
                styles_dict.update(self.config.parse_style_parameters(single_style[0], single_style[1]))
        return styles_dict

    def has_parent(self, name):
        current = self
        result = False
        while current.parent_storage:
            current = current.parent_storage
            result = result or current.tag.name == name
        return result

    def merge_parent_styles(self, style_storage):
        self.style.merge_parent(style_storage)

    def merge_less_priority_styles(self, style_storage):
        self.style.merge(style_storage)

    def get_block_styles(self):
        return {key: value for key, value in self.get_styles().iteritems() if key in self.config.block_style_processors}

    def get_styles(self):
        return self.style.values

    def get_classes(self):
        return self.classes.get_classes_until(1000)

    def get_single_style_value(self, name, default=None):
        return (self.style.values.get(name) or [default])[0]

    def apply_styles(self, vertex):
        text_style_processors = self.config.text_style_processors
        final_vertex = vertex
        styles = self.get_styles()
        sorted_keys = filter(lambda x: x in text_style_processors, styles.keys())
        sorted_keys = sorted(sorted_keys, key=lambda a: style_sorting_weight.get(a) or 10**9)
        for attribute in sorted_keys:
            for parameter in styles[attribute]:
                processor_fabric = text_style_processors[attribute]
                processor = processor_fabric.get_processor(final_vertex, parameter, self.config, self.globals)
                final_vertex = processor.as_vertex().add_child(final_vertex) if processor else final_vertex
        return final_vertex
