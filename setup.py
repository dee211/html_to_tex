from setuptools import setup, find_packages
from os.path import join, dirname

setup(
    name='html_to_tex',
    version='1.0',
    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README.txt')).read(),
    install_requires=['Jinja2==2.7.1', 'BeautifulSoup==3.2.1', 'path.py==7.0']
)