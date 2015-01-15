# -*- coding: utf-8 -*-
from converter import HtmlToTex
from settings import ConverterDefaultConfig


class TemplateToTexConverter(object):

    def __init__(self, template_path):
        self.template_path = template_path

    def convert(self):
        converter = HtmlToTex([ConverterDefaultConfig()])
        return converter.convert(open(self.template_path, 'r').read())

