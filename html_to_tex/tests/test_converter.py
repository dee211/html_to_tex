# -*- coding: utf-8 -*-
from os import system
import os
from tempfile import mkstemp
from unittest import TestCase
from helpers import TemporaryDirectory
from utils import TemplateToTexConverter


class TestUsability(TestCase):
    tests = [
        # 'libs/misc/tests/divs.html',
        # 'libs/misc/tests/escapes.html',
        # 'libs/misc/tests/text-styles.html',
        'libs/misc/tests/table.html',
        # 'libs/misc/html_to_tex/tests/lists.html',
        # 'libs/misc/html_to_tex/tests/colors.html',
    ]

    def test_everything(self):
        for test in self.tests:
            print u"Starting test %s" % test
            tex = TemplateToTexConverter(test).convert()
            self.assertIsNotNone(tex, u"Конвертация не удалась, test #%s" % test)
            with TemporaryDirectory() as tmp_folder:
                tex_file, tex_filename = mkstemp(dir=tmp_folder.name)
                # os.write(tex_file, tex.encode('utf-8'))
                # os.close(tex_file)
                # system(u"pdflatex {}".format(tex_filename))
                # system(u"okular {}.pdf".format(tex_filename))
                # system(u"evince {}.pdf".format(tex_filename))
