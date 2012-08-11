#!/usr/bin/env python
#
# Copyright John Reid 2009
#

"""
Code that reads in 2 sets of sequences and outputs those in the first that are not in the second.
"""


import sys, corebio.seq_io.fasta_io as F, corebio.seq
from optparse import OptionParser

#
# Parse the options
#
option_parser = OptionParser()
options, args = option_parser.parse_args()

#
# Check args
#
if 2 != len(args):
    print >> sys.stderr, 'USAGE: %s <fasta file> <fasta file>' % __file__
    sys.exit(-1)
fasta1, fasta2 = args

# read in second fasta
to_subtract = set(seq.description.strip().lower() for seq in F.iterseq(open(fasta2, 'r'), corebio.seq.dna_alphabet))

# read in first fasta
for seq in F.iterseq(open(fasta1, 'r'), corebio.seq.dna_alphabet):
    if seq.description.strip().lower() not in to_subtract:
        F.writeseq(sys.stdout, seq)
