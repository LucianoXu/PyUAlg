from pyualg import *


# The signature of the OML language.
oml_sig = Signature(
    {
        '1': (0, set()),
        '&': (2, {'Infix'}),
        '|' : (2, {'Infix'}),
        '~' :(1, set())
    }
)

parser = Parser(oml_sig)

def test_oml(term):
    term = parser.parse_term('((~ a) | (a & b))')