#!/usr/bin/env python
#
# Copyright John Reid 2009, 2010, 2011
#

"""
Code that reads in sequences from a FASTA file and prints information about them
"""


import sys, corebio.seq_io.fasta_io as F, corebio.seq, numpy
from optparse import OptionParser

#
# Parse the options
#
option_parser = OptionParser()
option_parser.add_option(
    '-t',
    '--tally',
    dest='do_tally',
    action='store_true',
    default=False,
    help="Tally the bases in each sequence."
)
options, args = option_parser.parse_args()

#
# Check args
#
if 0 == len(args):
    print >> sys.stderr, 'USAGE: %s <fasta file>' % __file__
    sys.exit(-1)

for fasta in args:

    #
    # Read the sequences
    #
    alphabet = corebio.seq.reduced_nucleic_alphabet
    if options.do_tally:
        tally = numpy.zeros(len(alphabet), dtype=int)
    num_bases = num_seqs = 0
    max_length = 0
    min_length = -1
    num_empty = 0
    for seq in F.iterseq(
        open(fasta, 'r'),
        alphabet
    ):
        num_seqs += 1
        num_bases += len(seq)
        if options.do_tally:
            tally += seq.tally()
        max_length = max(max_length, len(seq))
        if 0 == len(seq):
            num_empty += 1
        elif -1 == min_length or min_length > len(seq):
            min_length = len(seq)

    #
    # Print the information
    #
    print fasta
    print '%d sequences' % num_seqs
    print '%d bases' % num_bases
    print '%5.2f bases/sequence' % (num_bases/float(num_seqs))
    print '%d empty sequences' % num_empty
    print '%d bases in shortest non-empty sequence' % min_length
    print '%d bases in longest sequence' % max_length
    if options.do_tally:
        for base, count in zip(alphabet, tally):
            print "%s : %8d : %5.2f%%" % (base, count, 100.*count/num_bases)
    print
