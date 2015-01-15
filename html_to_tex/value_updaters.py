# -*- coding: utf-8 -*-


class AbstractStyleMerger(object):
    def merge_styles(self, old, new):
        return NotImplemented


class UniterMerger(AbstractStyleMerger):
    def merge_styles(self, old, new):
        return list(set(old or []) | set(new or []))


class ReplacerMerger(AbstractStyleMerger):
    def merge_styles(self, old, new):
        return new or old
