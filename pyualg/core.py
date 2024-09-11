from __future__ import annotations

from typing import Literal

Property = Literal['Infix']
class Signature:
    '''
    It defines the signature of a universal algebra.
    Here we do not use variable arity, because the constant arity is required when generating the term.
    '''
    def __init__(self, symbol_dict: dict[str, tuple[int, set[Property]]]):
        '''
        symbol_dict: a dictionary that maps a symbol to a tuple, consisting of the arity and a set of properties.
        '''
        if 'ID' in symbol_dict:
            raise ValueError("The symbol 'ID' is reserved.")
        
        self.symbol_dict : dict[str, tuple[int, set[Property]]] = symbol_dict

        # check the validity of the signature
        for symbol, (arity, properties) in symbol_dict.items():
            if arity < 0:
                raise ValueError(f"The arity of the symbol '{symbol}' is negative.")
            if 'Infix' in properties and arity != 2:
                raise ValueError(f"The symbol '{symbol}' is infix but not binary.")

    def __str__(self) -> str:
        return str(self.symbol_dict)
    
class Term:
    def __init__(self, head: str, args: tuple[Term, ...] = ()):
        self.head: str = head
        self.args: tuple[Term, ...] = args

    def __eq__(self, other):
        return isinstance(other, Term) and self.head == other.head and self.args == other.args
    
    def __hash__(self):
        return hash((self.head, self.args))
        # return 0 # fix the hash value
    
    def __str__(self):
        # for constants, return the string directly
        if not self.args:
            return self.head
        
        # return the string (data sub1 sub2 ... subn)
        return f"({self.head} {' '.join(map(str, self.args))})"
    
    def __repr__(self):
        return self.__str__()
    
    @property
    def is_atom(self) -> bool:
        return not self.args
    
    def __getitem__(self, pos: int|tuple[int, ...]) -> Term:
        '''
        getitem accepts a tuple of integers as the position and returns the corresponding subterm
        '''
        if isinstance(pos, int):
            return self.args[pos]
        else:
            if not pos:
                return self
            return self.args[pos[0]][pos[1:]]

__all__ = ['Property', 'Signature', 'Term']