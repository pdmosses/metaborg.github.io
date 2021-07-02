# Lexical

## Identifiers

Identifiers used as names of constructors and transformations have the form

```sdf3
ID = [a-zA-Z][a-zA-Z0-9\-\_]*
```

In particular, hyphens can be part of identifiers.

Identifiers cannot be followed by identifiers or keywords without intervening whitespace.

## Reserved Words

!!! todo
    provide list of reserved words

## Module Names

Module names can be sequences of identifiers separated by `/`.

## Integers

```sdf3
INT = [0-9]+
```

!!! check
    syntax of integers

## Whitespace

Spaces, tabs, and newlines are whitespace and can occur between any two tokens.

## Comments

Comments follow the C/Java tradition.
That is, the language supports single line comments after `//`

```stratego
// a single line comment
```

and multi-line comments between `/*` and `*/`

```stratego
/*
  a multi-line comment
  can be spread over multiple
  lines
 */
```

Comments can occur anywhere.

Multi-line comments cannot be nested currently.

!!! todo
    but this should be changed so that multi-line comments can be nested
