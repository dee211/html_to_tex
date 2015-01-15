# -*- coding: utf-8 -*-
# На данный момент используется лишь для совместимости с планами в моей голове
from style_storage import StyleStorage


class ClassStorage(object):
    parent = None

    def __init__(self, classes, config):
        self.value = classes
        self.config = config

    def add_parent(self, parent):
        self.parent = parent

    def get_classes_until(self, depth):
        current = self
        while (depth > 0) & current:
            yield current.value
            depth -= 1
            current = current.parent

    def get_classes(self, depth=0):
        current = self
        while (depth > 0) & current:
            depth -= 1
            current = current.parent
        return current.value

    def to_style(self):
        return StyleStorage({}, self.config)