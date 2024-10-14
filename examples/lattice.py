# The module for free lattice and order decision problems.

from pyualg import *

sig_lattice = Signature(
    {
        '&': (2, {'Infix'}),
        '|': (2, {'Infix'}),
    }
)

parser = Parser(sig_lattice)

def test_lattice():
    term1 = parser.parse_term('((a & b) & c)')
    term2 = parser.parse_term('(a & (b & c))')