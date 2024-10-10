from setuptools import setup

NAME = "epubpacker"

DESCRIPTION = 'A module to pack ePub3 format'


URL = 'https://github.com/meng89/' + NAME

CLASSIFIERS = [
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: Implementation :: CPython',
    'Programming Language :: Python :: Implementation :: PyPy',
    'Topic :: Software Development :: Libraries :: Python Modules',
]
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(name=NAME,
      version='2.0.2',
      description=DESCRIPTION,
      include_package_data=True,
      author='Chen Meng',
      author_email='ObserverChan@gmail.com',
      license='MIT',
      url=URL,
      packages=[NAME],
      install_requires=requirements,
      classifiers=CLASSIFIERS)
