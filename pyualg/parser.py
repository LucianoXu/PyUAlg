# create the parser for the given signature

from .core import Signature, Term
import ply.lex as lex, ply.yacc as yacc
import re

class Parser:
    def __init__(self, sig: Signature, **kwargs):
        self.sig = sig

        # build the lexer

        # map the literal strings to valid token names
        self.reserved = {}
        for i, symbol in enumerate(sig.symbol_dict.keys()):
            self.reserved[symbol] = f'TOK{i}'


        self.tokens = ['ID'] + list(self.reserved.values())
        self.literals = ['(', ')']
        def t_ID(t):
            r'[a-zA-Z_][a-zA-Z_0-9]*'
            t.type = self.reserved.get(t.value, 'ID')
            return t
        self.t_ID = t_ID

        for symbol in sig.symbol_dict.keys():
            self.__dict__['t_' + self.reserved[symbol]] = re.escape(symbol)

        self.t_ignore = ' \t'

        # use // or /* */ to comment
        def t_COMMENT(t):
            r'(/\*(.|[\r\n])*?\*/)|(//.*)'
            for c in t.value:
                if c == '\n' or c == '\r\n':
                    t.lexer.lineno += 1
        self.t_COMMENT = t_COMMENT

        def t_newline(t):
            r'[\r\n]+'
            t.lexer.lineno += len(t.value)
        self.t_newline = t_newline

        def t_error(t):
            raise ValueError(f"Illegal character '{t.value[0]}'")
        self.t_error = t_error

        self.lexer = lex.lex(module=self, **kwargs)

        # build the parser
        def p_ID(p):
            'expression : ID'
            p[0] = Term(p[1])
        self.p_ID = p_ID

        # Helper function to capture symbol, arity, and properties
        def create_production_function(symbol, arity, is_infix):
            if arity == 0:
                def f(p):
                    p[0] = Term(symbol)
                f.__doc__ = f'''
                    expression : {self.reserved[symbol]}
                    '''
            elif is_infix:
                def f(p):
                    p[0] = Term(symbol, (p[2], p[4]))
                f.__doc__ = f'''
                    expression : '(' expression {self.reserved[symbol]} expression ')'
                    '''
            else:
                def f(p):
                    p[0] = Term(symbol, p[3:3 + arity])
                f.__doc__ = f'''
                    expression : '(' {self.reserved[symbol]} {"expression "*arity} ')'
                    '''
            return f

        for i, symbol in enumerate(sig.symbol_dict.keys()):
            arity, properties = sig.symbol_dict[symbol]

            self.__dict__['p_' + str(i)] = create_production_function(symbol, arity, 'Infix' in properties)

        def p_error(p):
            if p:
                raise ValueError(f"Syntax error at '{p.value}'")
            else:
                raise ValueError("Syntax error at EOF")
            
        self.p_error = p_error

        self.start = 'expression'
        self.parser = yacc.yacc(module=self, **kwargs)

    def parse(self, input_string: str):
        res = self.parser.parse(input_string, lexer = self.lexer)
        if not res:
            raise ValueError(f"Parsing failed for the input string '{input_string}'")

        return res