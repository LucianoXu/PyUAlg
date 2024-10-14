# PyUAlg

A Python library for the lightweight framework of universal algebra, including signature, term syntax, parsing, matching and rewriting.

## Documentation

### `pyualg.Signature` 
A class for the signature of an algebraic structure. 

#### `Signature(symbol_dict: dict[str, tuple[int, set[Property]]])` 
is the constructor of the class. The input is a dictionary whose keys are the symbols of the signature and values are tuples of the arity and the set of properties of the symbols.

### `pyualg.Term` 
A class for the term syntax of an algebraic structure.

#### `Term(head: str, args: tuple[Term, ...] = ())`
The constructor of the class. The input is the head symbol of the term and a tuple of arguments.

#### `__eq__(other: Term) -> bool`
#### `__str__() -> str`
#### `sig_str(sig: Signature) -> str`
#### `__getitem__(self, pos: int|tuple[int, ...])`
Get the subterm of the term at the given position.

### `pyualg.unique() -> Term`
A function to generate unique variable names.


### `pyualg.Subst`
#### `Subst(self, data: dict[str, Term])`
#### `__call__(self, term: Term) -> Term`

### `pyualg.MatchingProblem`
#### `single_match(sig: Signature, lhs : Term, rhs : Term) -> Subst | None`

### `pyualg.RewriteRule`
#### `RewriteRule(lhs: Term, rhs: Term)`
#### `__call__(self, sig: Signature, term: Term) -> Optional[Term]`

### `pyualg.TRS`
#### `TRS(sig: Signature, rules: list[RewriteRule])`
#### `__call__(self, term: Term, alg: Literal["inner_most", "outer_most"] = "inner_most") -> Term`

### `pyualg.Parser`
#### `Parser(self, sig: Signature, **kwargs)`
#### `parse_term(input_string: str) -> Term`
#### `parse_rewriterule(self, input_string: str) -> RewriteRule`