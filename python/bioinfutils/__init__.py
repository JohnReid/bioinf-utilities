#
# Copyright John Reid 2012
#


"""
Some utilities.
"""

from functools import partial
import sys, corebio.seq, string


def shorten(seq, length):
    "Shorten the sequence to the given length."
    tag = '(shortened to %d)' % length
    if length > len(seq):
        raise ValueError('Sequence is too short: %d < %d' % (len(seq), length))
    return corebio.seq.Seq(
        seq[:length],
        name='%s %s' % (seq.name, tag),
        description='%s %s' % (seq.description, tag),
        alphabet=seq.alphabet,
    )


def strip_Ns(seq):
    "Strip Ns from beginning and end of the sequences."
    tag = '(stripped of Ns)'
    return corebio.seq.Seq(
        seq.strip('N'),
        name='%s (stripped of Ns)' % seq.name,
        description='%s (stripped of Ns)' % seq.description,
        alphabet=seq.alphabet,
    )



_translate_table = string.maketrans('acgt', 'NNNN')

def mask_lower(seq):
    "Create a new sequence where lower case A,C,G,T are replaced with Ns. Useful for masking UCSC data."
    return corebio.seq.Seq(
        seq.tostring().translate(_translate_table),
        name='%s (lower masked)' % seq.name,
        description='%s (lower masked)' % seq.description,
        alphabet=seq.alphabet,
    )



def open_fasta(fasta, default, mode):
    "Open a FASTA file or return default if fasta filename is '-'"
    if '-' == fasta:
        return default
    else:
        return open(fasta, mode)

open_input = partial(open_fasta, default=sys.stdin, mode='r')
open_output = partial(open_fasta, default=sys.stdout, mode='w')
