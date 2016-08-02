from setuptools import setup
from distutils.util import convert_path


NAME = "epubaker"

main_ns = {}
ver_path = convert_path('{}/version.py'.format(NAME))
with open(ver_path) as ver_file:
    exec(ver_file.read(), main_ns)

DESCRIPTION = 'A module to build EPUB 2 or 3 document.'


URL = 'https://github.com/meng89/' + NAME

CLASSIFIERS = [
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: Implementation :: CPython',
    'Programming Language :: Python :: Implementation :: PyPy',
    'Topic :: Software Development :: Libraries :: Python Modules',
]
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(name=NAME,
      version=main_ns['__version__'],
      description=DESCRIPTION,
      include_package_data=True,
      author='Chen Meng',
      author_email='ObserverChan@gmail.com',
      license='MIT',
      url=URL,
      packages=[
          'epubaker',
          'epubaker.metas',
          'epubaker.xl'
      ],
      install_requires=requirements,
      classifiers=CLASSIFIERS)
