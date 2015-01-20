# -*- coding: utf-8 -*-
import os
from jinja2 import Environment, FileSystemLoader
from html_to_tex.settings import root_path


env = Environment(loader=FileSystemLoader('/'))
