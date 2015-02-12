# -*- coding: utf-8 -*-
import os
from os.path import join
from platform import system
from tempfile import mkstemp
from unittest import TestCase
from html_to_tex import html_tex_converter
from html_to_tex.helpers import TemporaryDirectory
from html_to_tex.settings import root_path


class TestUsability(TestCase):
    tests = [
        # 'libs/misc/tests/divs.html',
        # 'libs/misc/tests/escapes.html',
        # 'libs/misc/tests/text-styles.html',
        'tests/examples/table.html',
        # 'libs/misc/html_to_tex/tests/lists.html',
        # 'libs/misc/html_to_tex/tests/colors.html',
    ]

    def test_everything(self):
        for test in self.tests:
            print u"Starting test %s" % test
            abs_path = join(root_path, test)
            test_file = open(abs_path, 'r')
            tex = html_tex_converter.convert(test_file.read())
            self.assertIsNotNone(tex, u"Конвертация не удалась, test #%s" % test)
            with TemporaryDirectory() as tmp_folder:
                tex_file, tex_filename = mkstemp(dir=tmp_folder.name)
                os.write(tex_file, tex.encode('utf-8'))
                os.close(tex_file)
                # system(u"pdflatex {}".format(tex_filename))
                # system(u"okular {}.pdf".format(tex_filename))
                # system(u"evince {}.pdf".format(tex_filename))
