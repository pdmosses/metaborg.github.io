# Lexical Syntax

The lexical syntax usually describes the low level structure of programs (often referred to as lexical tokens).
However, in SDF3, the token concept is not really relevant, since only character classes are terminals.
The lexical syntax sections in SDF3 are simply a convenient notation for the low level syntax of a language.
The ``LAYOUT`` symbol should also be defined in a lexical syntax section.
A lexical syntax consists of a list of productions.

Lexical syntax is described as follows::

```
lexical syntax

    <Production>*
```

An example of a production in lexical syntax:

```
lexical syntax

    BinaryConst = [0-1]+
```
