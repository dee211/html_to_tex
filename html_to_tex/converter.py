# -*- coding: utf-8 -*-
import os
from tempfile import mkstemp
from os import system
from subprocess import CalledProcessError
from BeautifulSoup import BeautifulSoup
from jinja2 import Markup
from constants import compilation_timelimit
from globals import ConverterGlobals
from jinja2_tools import env
from printer import TexPrinter
from settings import ConverterSafeConfig, ConverterDefaultConfig, ConverterSafestConfig
# from jinja2.views import JinjaTemplateView, render_to_string


class OutputProcessError(CalledProcessError):

    def __str__(self):
        return "Command '%s' returned non-zero exit status %d\nOutput:\n%s" % (self.cmd, self.returncode, self.output)


class HtmlToTex(object):
    configurations = []
    tag_processors = {}
    block_style_processors = {}
    text_style_processors = {}
    document_header = u""
    document_template = u""
    non_inherited_styles = {}

    def __init__(self, configurations=None, css=tuple()):
        self.css = css
        default_configurations = [ConverterDefaultConfig(), ConverterSafeConfig(), ConverterSafestConfig()]
        self.configurations = configurations or default_configurations

    def get_tex_error(self, tex):
        errors = TexPrinter(tex.encode('utf-8'), draft=True, time_limit=compilation_timelimit).do_operation()
        if errors:
            return errors

    def generate_tex(self, config, html):
        parsed = BeautifulSoup(html)
        processors_tree = config.get_tag_processor(tag=parsed, parent=None, globals=ConverterGlobals())
        processors_tree.build()
        tex = self.tree_to_tex(processors_tree, config)
        return tex

    def convert(self, html=u""):
        texs = (self.generate_tex(config, html) for config in self.configurations)
        error = None
        for tex in texs:
            error = self.get_tex_error(tex)
            if not error:
                return tex
        raise error

    def tree_to_tex(self, tree, config):
        context = self.get_context_data(tree, config)
        return Markup(env.get_template(config.template_name).render(context))

    def get_context_data(self, tree, config, **kwargs):
        return dict(
            document=u"".join(tree.as_vertex().get_iterator()),
            colors_defines=tree.globals.get_colors_defines()
        )


def html_to_pdf(html=u''):
    tex = HtmlToTex().convert(html)
    pdf = TexPrinter(tex.encode('utf-8'), draft=False).do_operation()
    return pdf

# if __name__ == '__main__':
#     from html_to_tex.utils import TemplateToTexConverter
#     tex = TemplateToTexConverter(template_name='libs/misc/html_to_tex/tests/psyco_pavlov_test.html').convert()
#     with TemporaryDirectory() as tmp_folder:
#         tex_file, tex_filename = mkstemp(dir=tmp_folder)
#         os.write(tex_file, tex)
#         os.close(tex_file)
#         system(u"pdflatex {}".format(tex_filename))
#         system(u"okular {}.pdf".format(tex_filename))
#         system(u"evince {}.pdf".format(tex_filename))
