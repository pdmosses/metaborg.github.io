# Patterns

## Term Patterns

A term _pattern_, is a [term](../terms/) extended with variables.

In the term pattern

```stratego
Plus(e, Int("0"))
```

the identifier `e` is a variable that stands for any term.

A pattern is _linear_ if each variable occurs at most once, _non-linear_ otherwise.
The _non-linear_ pattern

```stratego
Plus(e, e)
```

stands for a `Plus` term with identical arguments.

A term pattern without variables is _ground_.

## Substitution

_Substitution_ is the process of applying a map from variables to terms to a term pattern, replacing occurrence of variables in the domain of the map with the corresponding terms in the codomain of the map.

## Pattern Matching

_Pattern matching_ is the process of matching a ground term against a term pattern.

A term `t` matches a term pattern `p` iff there is a substition `S` such that applying the substitution to the pattern `S(p)` yields the term `t`.
