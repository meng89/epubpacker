from setuptools import setup
import os 

NAME = "epubuilder"

VERSION = '0.5.4'

DESCRIPTION = 'A library to write EPUB v3.'

LONG_DESCRIPTION = ''
if os.path.exists('long_description.rst'):
    LONG_DESCRIPTION = open('long_description.rst').read()


URL = 'https://github.com/meng89/{}'.format(NAME)

DOWNLOAD_URL = '{}/archive/v{}.tar.gz'.format(URL, VERSION)

CLASSIFIERS=['Development Status :: 4 - Beta',
             'Intended Audience :: Developers',
             'License :: OSI Approved :: MIT License',
             'Programming Language :: Python :: 3',
             'Topic :: Software Development :: Libraries :: Python Modules']

setup(name=NAME,
      version=VERSION,
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      author='Chen Meng',
      author_email='ObserverChan@gmail.com',
      license='MIT',
      url=URL,
      download_url=DOWNLOAD_URL,
      packages=['epubuilder'],
      install_requires=[line.strip() for line in open('requirements.txt')],
      classifiers=CLASSIFIERS
)
