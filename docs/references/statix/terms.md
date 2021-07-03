# Terms

In Statix, data is represented using terms. This data can be a program, a typing
annotation, or anything else that the specification defines. Terms are built from
atoms and composites, such as constructors, tuples and lists. Additionally, Statix
allows to inline several constraint results in terms.

In this section, we explain the various types of terms that Statix supports, and,
when appropriate, how their types should be declared.

!!! note "Terminology: Sort vs. Type"
    Throughout this reference manual, we use the term 'sort' for syntactic
    categories, and 'type' for all other types (such as lists, tuples, scopes, etc.).
    However, in practise, these terms are both used in both meanings.


## Numerals

Numeric literals are literals of the form `[0-9]+`. Negative literals are not
supported directly. All integer literals have the built-in type `int`.


## Strings

String literals are arbitrary, single-line sequences of characters enclosed in
double quotes. String literals may not contain unescaped backslashes, double
quotes, or tabs. Double quotes and backslashes can be used in a string literal
by prefixing them with another backslashes (`\"` and `\\`, respectively), while
tabs, newlines and carriage returns can be encoded using respectively `\t`, `\n`
and `\r`. Otherwise, no escaping is required. String literals have the built-in
type `string`.


## Identifiers

Variables are identifiers of values of the following form: `[a-zA-Z] [a-zA-Z0-9\_]* [\']*`.

With respect to type-checking, variables can be handled in two ways. When a variable
occurs in the [head of a rule](../rules#rule-definitions), it is implicitly
brought into scope with the type inferred from the rule type. Otherwise, it is
required that the variable is introduced earlier, with the correct type.
Apart from introduction in rule heads, variables can be introduced by
[existential constraints](../basic-constraints#exists). In that case, the type
of the variable is derived from its usage.


## Wildcards

Wildcards are represented as `_`, and denote variables without identity.
Every occurrence of a wildcard is interpreted as a new variable. Because
wildcards cannot reference each other, it is not required that the types of
multiple wildcard occurrences coincide.


## Composite terms

Composite terms can be build using _constructor applications_:

```statix
$ConsId({$Term ","}*)
```

Here a term with constructor `$ConsId` and some term arguments is built.

Composite terms must adhere to a signature. A signature describes which term
compositions are valid, and must be declared in a `signature` section:

```statix
signature
  sorts $SortID*

  constructors
    $ConsId : {$Type "*"}+ -> $SortID
    $ConsId : $SortID
```

First, the syntactic categories (which closely correspond to type identifiers in
other languages) must be declared in a `sorts` subsection. Then, the constructor
symbols can be declared in a `constructors` section. For each constructor, the
types of the arguments and its sort should be provided. For nullary constructors
(constructors without arguments), the arrow preceding the sort should be omitted.

When a composite term is built, it is validated that all arguments match the type
declaration from the signature. The type of the whole composite term is equal to
the sort of the constructor.


## Tuples

A built-in composite data construction is _tuples_:

```statix
({$Term ","}*)
```

Tuples have a statically fixed length, but the types of the arguments may differ.
The type of the tuple expression is just the product of its arguments.

The arity of a tuple may be anything except one, because unary tuples cause
syntactic ambiguities with bracketed expressions.


## Lists

Another built-in composite data construction is _lists_:

```statix
[{$Term ","}*]
```

Lists are created by comma-separating terms, enclosing them in square brackets.
All terms should have the same type. Given that the type of the terms is `T`, the
type of the list expression will be `list(T)`.

Alternatively, lists can have a variable tail:

```statix
[{$Term ","}* | $Term]
```

In this syntax, the tail of the list is another term. This term should have type
`list(T)`, where `T` is again the type of the first terms.


## Name Ascription

It is possible to assign names to terms by prefixing the term with a variable name:

```statix
$Var@$Term
```

Note that this does _not_ introduce a new variable with name `$Var` (except in a
[rule head](../rules#rule-definitions), where all variables are introduced
implicitly), but rather requires that a variable with corresponding name and type
is already introduced.

??? tip "Ascribe and Equality"
    In terms of [equality constraints](../basic-constraints#equality), the ascribe
    is equal to `$Var == $Term`. It is used to prevent the duplication of `$Term`.


## Type Ascription

Statix allows to add inline type annotations to terms as follows:

```statix
$Term : $Type
```

The type-checker will validate that the term actually has the specified type,
but the runtime behavior in not influenced by these ascriptions.

!!! tip "Complete Inference"
    In general, the Statix type-checker should be able to infer all types.
    However, in case of a type error being reported at an incorrect position,
    these type ascriptions can help tracing the cause of the error.


## Arithmetic operations

Arithmetic expressions can be inserted in terms as follows:

``` {.statix .no-ligatures}
#( $ArithExp )
```

Here, the type of the expression is `int`. For more information on arithmetic
expressions, see [Arithmetic Constraints](../basic-constraints#arithmetic-constraints)

??? tip "Normalization"
    In terms of [existential constraints](../basic-constraints#exists), inline
    arithmetic expressions have behavior equal to `{v} v #= $ArithExp`, where `v`
    is used at the position of the arithmetic expression. So, for example,
    `{T} T == CONS(#(21 * 2))` is equal to `{T v} v #= 21 * 2, T == CONS(v)`.


## AST Identifier

In Spoofax, all terms in an AST are assigned an unique identifier (the term index)
before analysis. This term identifier can be isolated as follows:

```statix
astId($Term)
```

Here, the type of `$Term` can be anything, and the type of the whole term will
be `astId`. AST Identifiers are used to assign [properties](../basic-constraints#ast-property).


## New

Statix allows inline creation of [scopes](../scope-graphs#scopes):

```statix
new
```

Statically, the `new` term has type `scope`. At runtime, this creates a fresh
scope, and inserts that at the position of the `new` term.

??? tip "Normalization"
    In terms of [existential constraints](../basic-constraints#exists), the inline
    `new` operator has behavior equal to `{s} new s`, where `s` is used at the
    position of the `new` term. So, for example, `{T} T == CLASS(new)` is equal
    to `{T s} new s, T == CLASS(s)`.


## Paths

Part of a [query result](../queries#result-pattern) is the path from the resolved
datum back to the scope where the query started. In order to represent paths,
Statix has two built-in constructors:

- `_PathEmpty`: Unary constructor that carries a single scope. This constructor
  has type `scope -> path`.
- `_PathStep`: Ternary constructor that represents a traversed edge in a path.
  This constructor has type `path * label * scope -> path`.

!!! note "Label Constraints"
    Although the labels in a `_PathStep` can be bound to a variable, and hence
    be compared with and included in other terms, no inspection, matching or
    comparison with label definitions is supported.


## Occurrences

!!! warning
    Since Spoofax 2.5.15, namespaces and occurrences are deprecated.

Statix has built-in support for namespaces. A term embedded in a particular
namespace is called an `occurrence`. Occurrences can be written as follows:

```statix
$NamespaceId{ $SpaceTerms }
$NamespaceId{ $SpaceTerms @$OccurrenceId }
```

In this structure template, `$SpaceTerms` means a list of terms, separated by
spaces. The occurrence identifier can be any term. In case the term has an AST
identifier, that value will be used as the identity of the occurrence.

Alternatively, the occurrence identifier can be left out:

```statix
$NamespaceId{ $SpaceTerms }
```

The default occurrence identifier is `-`, which means that the occurrence has no
identifier. The type of an occurrence literal is `occurrence`. For more information
about namespaces, see the [Queries](../queries) section.


## Declaration Match

Statix allows to query the current scope for declarations of a particular form:

```statix
?$RelationId[{$Term ","}] in $Scope
```

When using this expression, a _functional_ relation `$RelationId` must be declared.
The terms arguments must correspond to the argument of the relation, and the
type of the term is the output type of the relation.

For more information on querying the scope graph, see the [Queries](../queries) section.

??? tip "Declaration Match as Query"
    In terms of [regular queries](../queries), the declaration match is equal
    to a query with filter `e`, expecting a single output. E.g. `T == ?var["x"] in s`
    is equal to `query var filter e and { x' :- x' == "x" } in s |-> [(_, (_, T))]`.
