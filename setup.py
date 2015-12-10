# from distutils.core import setup
from setuptools import setup

from epubuilder import version

setup(name='epubuilder',
      version=version,
      description='A Library to write EPUB v3.',
      # long_description='',
      author='Chen Meng',
      author_email='observerchan@gmail.com',
      license='MIT',
      url='https://github.com/meng89/epubuilder',
      # py_modules=['epubuilder'],
      packages=['epubuilder'],
      classifiers=['Development Status :: 4 - Beta',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: MIT',
                   'Programming Language :: Python :: 3',
                   'Topic :: Software Development :: Libraries :: Python Modules'],
      install_requires=[
          'lxml',
          'magic',
      ]
      )
