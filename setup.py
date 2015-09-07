# coding=utf-8

from distutils.core import setup

from epubuilder import version


setup(name='epubuilder',
      version=version,
      description='Library to write files in the epub version 3.',
      # long_description='',
      author='Chen Meng',
      author_email='observerchan@gmail.com',
      license='MIT',
      url='https://github.com/meng89/epubuilder',
      py_modules=['epubuilder'],
      classifiers=['Development Status :: 4 - Beta',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: MIT',
                   'Programming Language :: Python :: 3',
                   'Topic :: Software Development :: Libraries :: Python Modules'],
      install_requires=[
          'lxml',
          'magic',
          'pillow',
      ]
      )
