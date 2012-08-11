#!/usr/bin/env python
#
# Copyright John Reid 2009
#

"""
Code that reads in sequences and shuffles them.
"""


import sys, corebio.seq_io.fasta_io as F, corebio.seq, numpy as N, numpy.random as R
from optparse import OptionParser


def is_unknown(x):
    "@return: True iff x == 4."
    return 4 == x


def partition(iterable, keyfunc=None):
    "Partition an iterable into groups for which keyfunc returns the same value. Yields (key, begin, end) tuples."
    if keyfunc is None:
        keyfunc = lambda x: x
    iterable = iter(iterable)
    lastkey = object()
    begin = None
    for i, x in enumerate(iterable):
        currkey = keyfunc(x)
        if currkey != lastkey:
            if None != begin:
                yield lastkey, begin, i
            begin = i
        lastkey = currkey
    if None != begin:
        yield lastkey, begin, i


def shuffle(seq):
    "@return: A shuffled version of the sequence leaving unknowns in place."
    ords = N.array(seq.ords())
    for key, begin, end in partition(ords, keyfunc=is_unknown):
        if not key:
            R.shuffle(ords[begin:end])
    shuffled = seq.alphabet.chrs(ords)
    shuffled.name = '%s (shuffled)' % seq.name,
    shuffled.description = '%s (shuffled)' % seq.description,
    shuffled.alphabet = seq.alphabet
    return shuffled


#
# Parse the options
#
option_parser = OptionParser()
options, args = option_parser.parse_args()


#
# Check args
#
if 1 != len(args):
    print >> sys.stderr, 'USAGE: %s <fasta file>' % __file__
    sys.exit(-1)
fasta = args[0]


#
# Shuffle the sequences
#
for seq in F.iterseq(
    open(fasta, 'r'),
    corebio.seq.dna_alphabet
):
    F.writeseq(sys.stdout, shuffle(seq))
