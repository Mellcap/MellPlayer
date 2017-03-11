#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
MellPlayer Setup

Created on 2017-03-09
@author: Mellcap
'''

from setuptools import setup, find_packages
VERSION = '0.1.1'

setup(
    name='MellPlayer',
    version=VERSION,
    packages=find_packages(),
    install_requires=[
        'requests',
        'pycrypto'
    ],

    entry_points={
        'console_scripts': [
            'mellplayer = mellplayer.start:main'
        ],
    },

    license='MIT',
    author='Mellcap',
    author_email='imellcap@gmail.com',
    url='https://github.com/Mellcap/MellPlayer',
    description='A tiny terminal player of NetEase-Music based on Python',
    keywords=['mellplayer', 'terminal', 'netease', 'playlist', 'music', 'cli', 'player'],
)
