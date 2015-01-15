# -*- coding: utf-8 -*-
from tag_processors import FixedWrapperTagProcessor, AddStylesTagProcessor


class AbstractElementConfig(object):
    cls = NotImplemented

    def __init__(self, cls):
        self.cls = cls


class BaseElementConfig(AbstractElementConfig):

    def __init__(self, cls):
        super(BaseElementConfig, self).__init__(cls)
        self.params = dict()

    def get_processor(self, **kwargs):
        raise NotImplemented


class TagConfig(BaseElementConfig):
    def get_processor(self, tag, parent, config, globals):
        return self.cls(tag=tag, parent=parent, config=config, globals=globals, **self.params)


class AddStylesTagConfig(TagConfig):

    def __init__(self, additional_styles, cls=AddStylesTagProcessor):
        super(AddStylesTagConfig, self).__init__(cls)
        self.params.update(additional_styles=additional_styles)


class FixedWrapperTagConfig(TagConfig):

    def __init__(self, begin, end, cls=FixedWrapperTagProcessor):
        super(FixedWrapperTagConfig, self).__init__(cls)
        self.params.update(begin=begin, end=end)
