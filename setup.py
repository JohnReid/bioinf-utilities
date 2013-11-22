#!/usr/bin/env python
# -*- coding: latin-1 -*-
#
# Copyright John Reid 2012
#

"""
distutils setup script
"""

from setuptools import setup

setup(
    name              = 'bioinf-utilities',
    version           = '1.3.24',
    description       = 'Some utilities for sequence analysis',
    long_description  = open('README.txt').read(),
    author            = 'John Reid',
    author_email      = 'johnbaronreid@netscape.net',
    scripts = [
        'scripts/bed-add-names',
        'scripts/bed-get-regions',
        'scripts/bed-info',
        'scripts/bedtools2fasta',
        'scripts/bgr2bed',
        'scripts/make-GREAT-bg',
        'scripts/seq-filter-empty',
        'scripts/seq-filter-short',
        'scripts/seq-head',
        'scripts/seq-info',
        'scripts/seq-mask-lower',
        'scripts/seq-match-lengths',
        'scripts/seq-shorten',
        'scripts/seq-shuffle',
        'scripts/seq-strip-Ns',
        'scripts/seq-subtract',
        'scripts/seq-tally',
        'scripts/seq-upper',
        'scripts/subsample',
    ],
    url               = 'http://sysbio.mrc-bsu.cam.ac.uk/group/index.php/John_Reid',
    package_dir       = {'': 'python'},
    packages          = ['bioinfutils', 'corebio'],
    install_requires  = ['cookbook'],
    package_data = {
        # Include corebio LICENSE
        'corebio': ['LICENSE.txt'],
}
)
