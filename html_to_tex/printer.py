# -*- coding: utf-8 -*-
from itertools import chain
import os
from subprocess import check_output, CalledProcessError, STDOUT
from tempfile import mkstemp
import re
from constants import timeout_return_code
from helpers import TemporaryDirectory
from settings import HOME_DIR, PROJECT_ROOT


def init_tex_environment():
    if HOME_DIR:
        os.putenv('HOME', HOME_DIR)
    os.putenv("TEXINPUTS", ".:{}:".format(PROJECT_ROOT.dirname() / "etc/tex_styles/"))


def get_tex_error_message(error_message):
    pattern = re.compile(r'!\s(?P<msg>.*)(.*\n)*l\.[0-9]+(?P<place>(.*\n){2})')
    match = pattern.search(error_message, re.UNICODE)
    if match:
        error_text = match.group('msg').strip()[:-1]
        fragment = match.group('place').strip().split('...')
        fragment = fragment[1] if len(fragment) > 1 else fragment[0]
        return '{}\n"{}"'.format(error_text, fragment)
    return error_message


class TexPrinter(object):

    def __init__(self, content, draft, time_limit=u'0', passes=1):
        self.content = content
        self.draft = draft
        self.passes = passes
        self.time_limit = time_limit
        init_tex_environment()

    def generate_source_file(self, directory):
        tex_file, tex_filename = mkstemp(dir=directory)
        os.write(tex_file, self.content)
        os.close(tex_file)
        return tex_filename

    def get_command(self, filename):
        command = ['timeout', self.time_limit, '/usr/bin/pdflatex']
        args = ['-halt-on-error']
        if self.draft:
            args.append('-draftmode')
        return list(chain(command, args, [filename]))

    def do_operation(self):
        with TemporaryDirectory() as tmp_folder:
            tex_filename = self.generate_source_file(tmp_folder.name)
            try:
                command = self.get_command(tex_filename)
                for x in xrange(self.passes):
                    check_output(command, cwd=tmp_folder.name, stderr=STDOUT)
                if not self.draft:
                    with open(tex_filename + '.pdf', 'r') as f:
                        return f.read()
            except CalledProcessError as e:
                log_template = 'Latex error tex:\n{}'
                if e.returncode == timeout_return_code:
                    log_template = 'Latex timeout termination:\n{}'
                error = get_tex_error_message(e.output)
                return log_template.format(error)
