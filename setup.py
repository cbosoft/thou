#!/usr/bin/env python

from distutils.core import setup

setup(name='thou',
      version='0.1',
      description='a toy search engine',
      author='Chris Boyle',
      author_email='cbosoft@protonmail.com',
      url='https://github.com/cbosoft/thou',
      install_requires=['requests', 'beautifulsoup4'],
      packages=['thou'],
      scripts=['crawler', 'server']
     )
