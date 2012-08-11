#!/usr/bin/env python
#
# Copyright John Reid 2009,2010
#

"""
Code that reads in sequences and outputs first so many
"""


import sys, corebio.seq_io.fasta_io as F, corebio.seq
from optparse import OptionParser

#
# Parse the options
#
option_parser = OptionParser()
option_parser.add_option(
    "-n",
    "--num-seqs",
    dest="num_seqs",
    default=10,
    type='int',
    help="Number of sequences to output."
)
options, args = option_parser.parse_args()

#
# Check args
#
if 1 != len(args):
    print >> sys.stderr, 'USAGE: %s <fasta file>' % __file__
    sys.exit(-1)
fasta = args[0]
if '-' == fasta:
    input = sys.stdin
else:
    input = open(fasta, 'r')

for i, seq in zip(xrange(options.num_seqs), F.iterseq(input, corebio.seq.dna_alphabet)):
    F.writeseq(sys.stdout, seq)
