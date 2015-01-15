# -*- coding: utf-8 -*-
from itertools import chain
from misc import plain_to_tex


class BaseLatexTreeNode(object):

    def get_content(self, depth=0):
        raise NotImplementedError

    def ladder(self, value, depth):
        if value:
            return u"{}{}%\n".format(u" " * (4 * depth), value)
        return u""

    def get_iterator(self, depth=0):
        pass

    def add_child(self, child):
        raise TypeError("Node without children")


class LatexTreeNode(BaseLatexTreeNode):

    def __init__(self, open_sequence, close_sequence, force_create=False):
        super(LatexTreeNode, self).__init__()
        self.open_sequence = open_sequence
        self.close_sequence = close_sequence
        self.children = []
        self.force_create = force_create

    def fix_content(self, content):
        if isinstance(content, chain):
            try:
                deleted_value = content.next()
                content = chain([deleted_value], content)
            except StopIteration:
                content = []
        return content

    def add_child(self, child):
        self.children.append(child)
        return self

    def get_iterator(self, depth=0):
        content = self.get_content(depth)
        content = self.fix_content(content)
        if not (content or self.force_create):
            pass
        else:
            yield self.ladder(self.open_sequence, depth)
            for item in content:
                yield item
            yield self.ladder(self.close_sequence, depth)

    def get_content(self, depth=0):
        child_contents = (child.get_iterator(depth + bool(self.open_sequence)) for child in self.children)
        result = chain(*(child_content for child_content in child_contents if child_content))
        return result


class LatexTreeVoidNode(BaseLatexTreeNode):

    def __init__(self):
        super(LatexTreeVoidNode, self).__init__()

    def get_content(self, depth=0):
        return []


class LatexTreeExactLeaf(BaseLatexTreeNode):

    def __init__(self, value):
        super(LatexTreeExactLeaf, self).__init__()
        self.original_value = value
        value = self.prepare_value(value)
        if value and not value in (u"{}", u"{ }"):
            self.content = value
        else:
            self.content = u""
        self.children = []

    def prepare_value(self, value):
        return value

    def get_content(self, depth=0):
        return self.ladder(self.content, depth) if self.content else u""

    def get_iterator(self, depth=0):
        content = self.get_content(depth)
        if content:
            yield content


class LatexTreeLeaf(LatexTreeExactLeaf):

    def prepare_value(self, value):
        value = value.replace(u"\n", u" ")
        value = u"{%s}" % plain_to_tex(value)
        return value
