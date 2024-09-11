from .parser import *

def test_parser():
    sig = Signature(
        {
            'c': (0, set()),
            'f': (2, set()),
            'g': (1, set()),
            '+' : (2, {'Infix'}),
        }
    )

    parser = Parser(sig)
    assert str(parser.parse('c')) == 'c'
    assert str(parser.parse('((f (g x) y) + z)')) == '(+ (f (g x) y) z)'