#!/usr/bin/env python
#
# Copyright John Reid 2009,2010
#

"""
Code that reads in sequences from a FASTA file and shortens each sequence.
"""


import sys, corebio.seq_io.fasta_io as F, corebio.seq
from optparse import OptionParser



def shorten(seq):
    "@return: A shortened version of the sequence."
    return corebio.seq.Seq(
        seq[:length],
        name='%s (shortened)' % seq.name,
        description='%s (shortened)' % seq.description,
        alphabet=seq.alphabet,
    )


#
# Parse the options
#
option_parser = OptionParser()
option_parser.add_option(
    '-m',
    '--max-sequences',
    dest='max_seqs',
    type='int',
    default=-1,
    help="Set a limit on the number of sequences output."
)
options, args = option_parser.parse_args()

#
# Check args
#
if 2 != len(args):
    print >> sys.stderr, 'USAGE: %s <fasta file> <max sequence length>' % __file__
    sys.exit(-1)

fasta = args[0]
length = int(args[1])
if '-' == fasta:
    input = sys.stdin
else:
    input = open(fasta, 'r')

#
# Read the sequences
#
alphabet = corebio.seq.reduced_nucleic_alphabet
for i, seq in enumerate(F.iterseq(input, alphabet)):
    if options.max_seqs == i:
        break
    F.writeseq(sys.stdout, shorten(seq))
