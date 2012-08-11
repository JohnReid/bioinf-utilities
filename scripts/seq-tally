#!/usr/bin/env python
#
# Copyright John Reid 2009, 2012
#

"""
Code that reads in sequences from a FASTA file and counts occurrences of characters.
"""


import sys, corebio.seq_io.fasta_io as F, corebio.seq, numpy

for fasta in sys.argv[1:]:
    #
    # Tally the sequences
    #
    alphabet = corebio.seq.reduced_nucleic_alphabet
    tally = numpy.zeros(len(alphabet), dtype=int)
    num_seqs = 0
    for seq in F.iterseq(
        open(fasta, 'r'),
        alphabet
    ):
        tally += seq.tally()
        num_seqs += 1
    
    #
    # Get number of known bases
    #
    num_known = tally[:4].sum()
    percentages = tally * 100. / num_known
    
    #
    # Print the tally out
    #
    print fasta
    print "    %8d bp in %d sequences" % (tally.sum(), num_seqs)
    for base, count, percentage in zip(alphabet, tally, percentages):
        print "%s : %8d : %5.1f%%" % (base, count, percentage)
    print "GC-content   : %5.1f%%" % (percentages[1] + percentages[2])
    print
