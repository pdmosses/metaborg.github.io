---
title: "Terms"
---
# Terms
Within Spoofax, the programs are represented as Abstract Syntax Trees (ASTs).  This is an in-memory representation that uses ATerms (Annotated Term Format).  ATerms provide a common set of contructs to represent abstract trees, comparable to XML or algebraic data types in functional programming languages.  It is based on the ATerms of Van den Brand et al.[@BrandJKO00], and has both textual and binary representations.

As an example, this is one possible representation of the expression `4 + f(5 * x)` as a term:

```terms
Plus(Int("4"), Call("f", [Mul(Int("5"), Var("x"))]))
```

A term `t` is constructed from the following elements:

- Constructor application: `#!terms C(t1, .., tN)`
- Tuple: `#!terms (t1, .., tN)`
- List: `#!terms [t1, .., tN]`
- String: `#!terms "foobar"`
- Integer: `#!terms 42`
- Real: `#!terms 13.37`
- Annotations: `#!terms t{t1, .., tN}`

## Constructor Application
A _constructor_ is an identifier.  It must be an alphanumeric string starting with a letter, or it can be double-quoted string.

A _constructor application_ `#!terms c(t1, .., tN)` creates a term by applying the constructor `c` to the list of zero or more term `t1, .., tN`.  For example, the term `#!terms Plus(Int("4"), Var("x"))` uses the constructors `Plus`, `Int`, and `Var` to create a nested term from the strings `"4"` and `"x"`.

A _tuple_ is just a special case of a constructor application where there is no constructor.

## List
A _list_ is a term of the form `#!terms [t1, .., tN]`. That is, a list of zero or more terms written between square brackets.  While all applications of a specific constructor typically have the same number of subterms but of varying types, lists can have a variable number of subterms typically of the same type.

An example of a list with two terms is shown in:

```terms
Call("f"), [Int("5"), Var("x")]
```

## Literal
An _integer_ literal is a whole number. For example, `#!terms 1`, `#!terms 12345`.

A _real_ literal is a number that includes a decimal dot `.`, and optionally an exponent. Examples include: `#!terms 12.2`, `#!terms .4`, `#!terms 14.0000001`, `#!terms 0.1e12`, `#!terms 13.37E15`.

A _string_ literal is a sequence of characters written between double quotes. For example, `#!terms "foobar"`.

## Annotation
While the term elements above are used to create the structural part of terms, a term can also be annotated with a list of terms.  These annotations typically carry additional semantic information about the term.  A term `t` annotated with a list `t1, .., tN` has the form `t{t1, .., tN}`.  The contents of an annotation is up to the application.

Example where the constructor application of `Lt` is annotated with a term describing the type of the expression `Type("bool")`:

```terms
Lt(Var("n"),Int("1")){Type("bool")}
```

\bibliography