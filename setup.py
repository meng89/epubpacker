from setuptools import setup
from distutils.util import convert_path
import os 

NAME = "epubuilder"

main_ns = {}
ver_path = convert_path('{}/version.py'.format(NAME))
with open(ver_path) as ver_file:
    exec(ver_file.read(), main_ns)

# DESCRIPTION = 'A library to write EPUB v3.'

LONG_DESCRIPTION = ''
if os.path.exists('long_description.rst'):
    LONG_DESCRIPTION = open('long_description.rst').read()


URL = 'https://github.com/meng89/{}' + NAME

CLASSIFIERS = ['Development Status :: 4 - Beta',
               'Intended Audience :: Developers',
               'License :: OSI Approved :: MIT License',
               'Programming Language :: Python :: 3',
               'Topic :: Software Development :: Libraries :: Python Modules']

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(name=NAME,
      version=main_ns['__version__'],
      # description=DESCRIPTION,
      # long_description=LONG_DESCRIPTION,
      include_package_data=True,
      author='Chen Meng',
      author_email='ObserverChan@gmail.com',
      license='MIT',
      url=URL,
      packages=['epubuilder'],
      install_requires=requirements,
      classifiers=CLASSIFIERS)
