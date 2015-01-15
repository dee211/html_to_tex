# -*- coding: utf-8 -*-
from tag_configs import BaseElementConfig
from style_processors import FixedStyleProcessor, BlockStyleProcessor


class StyleConfig(BaseElementConfig):
    def get_processor(self, tag, parameter, config, globals):
        return self.cls(tag=tag, parameter=parameter, config=config, globals=globals, **self.params)


class FixedWrapperStyleConfig(StyleConfig):

    def __init__(self, rules, cls=FixedStyleProcessor):
        super(FixedWrapperStyleConfig, self).__init__(cls)
        self.params.update(rules=rules)


class BlockStyleConfig(StyleConfig):

    def __init__(self, parameter_name, cls=BlockStyleProcessor):
        super(BlockStyleConfig, self).__init__(cls)
        self.params.update(parameter_name=parameter_name)
