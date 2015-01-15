# -*- coding: utf-8 -*-


class AbstractParametersParser(object):

    def get_elementary_styles(self, value, name):
        raise NotImplemented

    def parse(self, value):
        return value.split()


class OtherParametersParser(AbstractParametersParser):

    def get_elementary_styles(self, value, name):
        value = self.parse(value)
        return {name: [parameter for parameter in value]}


class BackgroundColorParametersParser(OtherParametersParser):

    def parse(self, value):
        return [value.strip(u" ")]


class NumberParametersParser(OtherParametersParser):
    def __init__(self, ending=u""):
        self.ending = ending

    def parse(self, value):
        return [value.strip(u" ")]

    def get_elementary_styles(self, value, name):
        value = self.parse(value)
        return {name: [self.fix_number(parameter) for parameter in value if self.fix_number(parameter)] }

    def fix_number(self, number):
        # TODO: учесть em, pt и прочие единицы измерения
        if number.endswith(u"px"):
            number = number[:-2]
        if number.endswith(u"%"):
            number = u""
        return number + self.ending
