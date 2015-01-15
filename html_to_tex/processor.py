# -*- coding: utf-8 -*-


class AbstractProcessor(object):
    force_create = False
    end = u""
    begin = u""

    def __init__(self, tag, parameter, config, globals):
        self.tag = tag
        self.config = config
        self.parameter = parameter
        self.globals = globals

    def get_begin(self):
        return self.begin

    def get_end(self):
        return self.end

    def as_vertex(self):
        raise NotImplementedError