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
        seq.strip('Nn'),
        name='%s (stripped of Ns)' % seq.name,
        description='%s (stripped of Ns)' % seq.description,
        alphabet=seq.alphabet,
    )



_lower_mask_table = string.maketrans('acgt', 'NNNN')

def mask_lower(seq):
    "Create a new sequence where lower case A,C,G,T are replaced with Ns. Useful for masking UCSC data."
    return corebio.seq.Seq(
        seq.tostring().translate(_lower_mask_table),
        name='%s (lower masked)' % seq.name,
        description='%s (lower masked)' % seq.description,
        alphabet=seq.alphabet,
    )



_upper_table = string.maketrans('acgtn', 'ACGTN')

def upper(seq):
    "Create a new sequence where lower case A,C,G,T are replaced with upper case. Useful for masking UCSC data."
    return corebio.seq.Seq(
        seq.tostring().translate(_upper_table),
        name=seq.name,
        description=seq.description,
        alphabet=seq.alphabet,
    )



def file_opener(filename):
    """Returns a function to open the file. Will check if filename ends in ".gz",
    if so it will return gzip.open.
    """
    if filename.endswith('.gz'):
        import gzip
        return gzip.open
    else:
        return open


def open_potentially_gzipped(filename, mode):
    """Opens the file. Handles compressed files by testing if the filename
    ends in ".gz"
    """
    return file_opener(filename)(filename, mode)


def open_fasta(fasta, default, mode):
    "Open a FASTA file or return default if fasta filename is '-'"
    if '-' == fasta:
        return default
    else:
        return open_potentially_gzipped(fasta, mode)

open_input = partial(open_fasta, default=sys.stdin, mode='r')
open_output = partial(open_fasta, default=sys.stdout, mode='w')
