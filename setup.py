#!/usr/bin/env python
# -*- coding:utf-8 -*-

from setuptools import setup, find_packages

from opps import facebookcomments


install_requires = ["opps", "facepy"]

classifiers = ["Development Status :: 4 - Beta",
               "Intended Audience :: Developers",
               "License :: OSI Approved :: MIT License",
               "Operating System :: OS Independent",
               "Framework :: Django",
               'Programming Language :: Python',
               "Programming Language :: Python :: 2.7",
               "Operating System :: OS Independent",
               "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
               'Topic :: Software Development :: Libraries :: Python Modules']

try:
    long_description = open('README.md').read()
except:
    long_description = facebookcomments.__description__

setup(
    name='opps-facebook-comments',
    namespace_packages=['opps', 'opps.facebookcomments'],
    version=facebookcomments.__version__,
    description=facebookcomments.__description__,
    long_description=long_description,
    classifiers=classifiers,
    keywords='poll opps cms django apps magazines websites facebook',
    author=facebookcomments.__author__,
    author_email=facebookcomments.__email__,
    url='http://oppsproject.org',
    download_url="https://github.com/yacows/opps-facebook-comments/tarball/master",
    license=facebookcomments.__license__,
    packages=find_packages(exclude=('doc', 'docs',)),
    package_dir={'opps': 'opps'},
    install_requires=install_requires,
)
