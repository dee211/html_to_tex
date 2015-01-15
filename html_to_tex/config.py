# -*- coding: utf-8 -*-


class BaseConfig(object):
    tag_processors = dict()
    text_style_processors = dict()
    block_style_processors = dict()
    parameters_parsers = dict()
    template_name = "tex_template/tex_document.tex"
    inherited_styles = {
        u"text-color",
        u'text-decoration',
        u'font-size',
        u'other',
        u'font-style',
        u'font-weight',
        u'sub',
        u'sup',
        u'color',
        u'text-background-color'
    }
    tag_types_by_node_cls = {
        u'NavigableString': u"text",
        u'Declaration': u"script",
        u'Comment': u"script",
    }

    def get_tag_processor(self, tag, parent, globals):
        name = self.tag_types_by_node_cls.get(tag.__class__.__name__) or tag.name
        name = name if name in self.tag_processors else u'other'
        return self.tag_processors[name].get_processor(tag=tag, parent=parent, config=self, globals=globals)

    def parse_style_parameters(self, style, parameters):
        parser = self.parameters_parsers[style if style in self.parameters_parsers else 'other']
        return parser.get_elementary_styles(parameters, style)
