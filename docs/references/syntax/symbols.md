# Symbols

The building block of SDF3 productions is a symbol.
SDF3 symbols can be compared to terminals and non-terminals in other grammar formalisms.
The elementary symbols are character classes, literals, and sorts.

Intrinsically, only character classes are real terminal symbols.
All other symbols represent non-terminals.
SDF3 also support symbols that capture BNF-like notation such as lists, optionals, alternatives, and sequences.
Note that these symbols are also non-terminals, and are just shorthands for common structures present in context-free grammars.

## Character classes

Character classes occur only in lexical syntax and are enclosed by ``[`` and ``]``.
A character class consists of a list of zero or more characters (which stand for themselves) such as ``[x]`` to represent the character ``x``,  or character ranges, as an abbreviation for all the characters in the range such as ``[0-9]`` representing ``0``, ``1``, ..., ``9``. A valid range consists of ``[c1-c2]``, where the character ``c2`` has a higher ASCII code than ``c1``. Note that nested character classes can also be concatenated within the same character class symbol, for example ``[c1c2-c3c4-c5]`` includes the characters ``c1`` and the ranges ``c2-c3``, ``c4-c5``. In this case, the nested character classes do not need to be ordered, as SDF3 orders them when performing a normalization step.

**Escaped Characters**: SDF3 uses a backslash (``\``) as a escape for the quoting
of special characters. One should use ``\c`` whenever ``c`` is not a digit or a letter
in a character class.

Arbitrary Unicode code points can be included in a character class by writing an escaped integer,
which is particularly useful for representing characters outside the printable ASCII range.
The integer can be a binary, octal, decimal, or hexadecimal number, for example:
``\0b101010``, ``\052``, ``\42``, and ``\0x2A`` all represent the code point 42,
or the ``'*'`` character.

Additionally, special ASCII characters are represented by:

- ``\t`` : horizontal tabulation
- ``\n`` : newline character
- ``\v`` : vertical tabulation
- ``\f`` : form feed
- ``\r`` : carriage return

**Character Class Operators**: SDF3 provides the following operators for character
classes:

- (complement) ``~`` : Accepts all the characters that are *not* in the original class.
- (difference) ``/`` : Accepts all the characters in the first class unless they are in a second class.
- (union) ``\/`` : Accepts all the characters in either character classes.
- (intersection) ``/\`` : Accepts all the characters that are accepted by both character classes.

Note that the first operator is unary and the other ones are left associative binary
operators. Furthermore, such operators are not applicable to other symbols in general.

## Literals

A literal symbol defines a fixed length word. This usually corresponds to a
terminal symbol in ordinary context-free grammars, for example ``"true"`` or
``"+"``. Literals must always be quoted and consist of (possibly escaped)
ASCII characters.

As literals are also regular non-terminals, SDF3 automatically generates productions
for them in terms of terminal symbols.

```
"definition" = [d][e][f][i][n][i][t][i][o][n]
```

Note that the production above defines a case-sensitive implementation of the defined literal.
Case-insensitive literals are defined using single-quoted strings as in ``'true'`` or ``'else'``.
SDF3 generates a different production for case-insensitive literals as

```
'definition' = [dD][eE][fF][iI][nN][iI][tT][iI][oO][nN]
```

The literal above accepts case-insensitive inputs such as ``definition``, ``DEFINITION``, ``DeFiNiTiOn`` or ``defINITION``.

## Sorts

A sort corresponds to a plain non-terminal, e.g. ``Statement`` or ``Exp``.
Sort names start with a capital letter and may be followed by letters, digits, hyphens, or underscores.
Note that unlike SDF2, SDF3 does not support parameterized sorts (yet!).

Sorts are declared by listing their name in the appropriate sorts section, which have the following forms.

For context-free sorts:

```
context-free sorts

    <Sort>*
```

For lexical sorts:

```
lexical sorts

    <Sort>*
```

SDF3 also supports kernel sorts:

```
sorts

    <Sort>*
```

!!! note
    Kernel sorts should be suffixed with ``-CF`` or ``-LEX``,
    depending on whether they are context-free sorts or lexical sorts.
    When a sort in a ``sorts`` block does not have a suffix, it is treated
    as a context-free sort.

Writing a sort in these sections only indicates that a sort has been declared, even if it does not have any explicit production visible.

## Optionals

SDF3 provides a shorthand for describing zero or exactly one occurrence of a sort by appending the sort with ``?``.

For example, the sort ``Extends?`` can be parsed as ``Extends`` or without consuming any input. Internally, SDF3 generates the following productions after normalizing the grammar::

     Extends?.None =
     Extends?.Some = Extends

Note that using ``?`` adds the constructors ``None`` and ``Some`` to the final abstract syntax tree.

## Lists

Lists symbols as the name says, indicate that a symbol should occur several times.
In this way, it is also possible to construct flat structures to represent them.
SDF3 provides support for two types of lists, with and without separators.
Furthermore, it is also possible to indicate whether a list can be empty (``*``) or should have at least one element (``+``). For example, a list ``Statement*`` indicates zero or more ``Statement``, whereas a list with separator ``{ID ","}+`` indicates one or more ``ID`` separated by ``,``. Note that SDF3 only supports literal symbols as separators.

Again, SDF3 generates the following productions to represent lists, when normalizing the grammar.

```
Statement* =
Statement* = Statement+
Statement+ = Statement+ Statement
Statement+ = Statement

{ID ","}* =
{ID ","}* = {ID ","}+
{ID ","}+ = {ID ","}+ "," {ID ","}
{ID ","}+ = {ID ","}
```

When parsing a context-free list, SDF3 produces a flattened list as an AST node such as ``[Statement, ..., Statement]`` or ``[ID, ..., ID]``. Note that because the separator is a literal, it does not appear in the AST.

## Alternative

Alternative symbols express the choice between two symbols, for example, ``ID | INT``.
That is, the symbol ``ID | INT`` can be parsed as either ``ID`` or ``INT``.
For that reason, SDF3 normalizes alternatives by generating the following productions:

```
ID | INT = ID
ID | INT = INT
```

Note that SDF3 only allow alternative symbols to occur in lexical syntax.
Furthermore, note that the alternative operator is right associative and binds stronger than any operator.
That is, ``ID "," | ID ";"`` expresses ``ID ("," | ID) ";"``.
To express ``(ID ",") | (ID ";")``, we can use a sequence symbol.

## Sequence

A sequence operator allows grouping of two or more symbols.
Sequences are useful when combined with other symbols such, lists or optionals, for example ``("e" [0-9]+)?``.
Like alternative symbols, sequences can only occur in lexical syntax.
A sequence symbol is normalized as

```
("e" [0-9]+) = "e" [0-9]+
```

## Labeled symbols

SDF3 supports decorating symbols with labels, such as ``myList:{elem:Stmt ";"}*``.
The labels have no semantics but can be used by other tools that use SDF3 grammars as input.

## ``LAYOUT``

The ``LAYOUT`` symbol is a reserved sort name. It is used to indicate the whitespace that can appear in between context-free symbols. The user must define the symbol ``LAYOUT`` such as:

```
LAYOUT = [\ \t\n]
```

Note that the production above should be defined in the lexical syntax.
