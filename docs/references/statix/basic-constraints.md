# Basic Constraints

As mentioned in the [Language Concepts](../language-concepts) section, the core
idea of Statix is to see a type-checking problem as a constraint solving problem.
Therefore, it is crucial to be able to express constraints in a specification.

In this section, we discuss all constraints that are note related to scope graphs.
These constraints are explained in-depth in the sections on [Scope Graph
Construction](../scope-graphs) and [Queries](../queries).


## True

```statix
true
```

The `true` constraint is the constraint that is trivially satisfied.


## False

```statix
false $Message?
```

The `false` constraint is the constraint that will always fail. Just as all other
constraints that can fail, it is possible to add a [message](#messages).


## Conjunction

```statix
$Constraint,
$Constraint
```

A conjunction of constraints is satisfied when both conjuncts are satisfied.
Note that the solving order of the conjuncts is undefined.


## Equality

```statix
$Term == $Term $Message?
```

Asserts that two terms are equal. When necessary, this constraint infers values
for free variables in the terms. Statically, both terms should have the same type.

## Disequality

```statix
$Term != $Term $Message?
```

Asserts that two terms are not equal. Statically, both terms should have the same type.

Statix treats free variables as different from each other, and as different from
concrete terms. Therefore, when any of both terms is not ground (i.e. contains
free variables), the constraint will _not_ fail.


## Exists

```statix
{ $Var* }
  $Constraint
```

An exists constraint introduces new existentially quantified variables in the
scope of its subconstraint. The names of the variables in an exists constraint
should be unique (i.e. `{x x} true` is not allowed), but are allowed to shadow
outer variables.


## Try

```statix
try { $Constraint } $Message?
```

The `try` constraint validates whether the outer context implies that the inner
constraint holds. That is: any model for the outer context (all other constraints
than `$Constraint`) is also a (not necessarily minimal) model for `$Constraint`.

In order to implement these semantics, the `$Constraint` is handled differently
than regular constraints in two ways.

1. The `$Constraint` is _not_ allowed to refine the outer context. Therefore,
   equality constraints will not infer values for variable that were introduced
   outside the `try`. Likewise, scopes can not be instantiated, nor edges/declarations
   added to scopes from outside the `try`. This behavior also implies that values
   constructed within a `try` construct will never escape the `try` context.
2. Disequalities in `$Constraint` that involve free variables cause the `try`
   to fail, because appearently the disequality does not hold for all models of
   the outer context.

!!! todo
    Explain the design choices for `try` in a background section.


## AST Identifiers

```statix
astId($Term, $Term)
```

The `astId` constraint asserts that its second argument is the term index of the
first argument. The type of the first argument may be anything, but the type of
the second argument is `astId`.

!!! tip
    Often, using an [`astId` _term_](../terms#ast-identifier) will read more natural.


## AST Property


```statix
@$Term.$Prop $Op $Term
```

Statix allows to set properties on AST nodes. These properties can be used to
communicate typing results to the outside world, for example to be used in
a transformation. For more information on reading these properties, please refer
to the [Stratego API documentation](../stratego-api).

The first term is the term (usually an AST node) on which the property is set.

Next `$Prop` specifies which property is set. This property can be any string
of the form `[a-zA-Z] [a-zA-Z0-9\_]*`. It is not required to declare properties.

There are two special properties: `ref` and `type`. `ref` properties are set on
(syntactic) variable references, and point to the term they are referencing. The
Spoofax reference resolution service uses these properties to offer reference
resolution in the editor. The `type` property contains the type of a term. This
type is shown when hovering over a term in an editor.

The `$Op` specifies the operator with which a property is set. There are two
possible operators:

- `:=`: The assignment operator. This operator requires a property to have only
  a single unique value (although, since Spoofax 2.5.17, that value may be set
  multiple times).
- `+=`: The bag insertion operator. Properties using this operator can be set
  multiple times, and will be aggregated in the eventual property value.

Note that using both operators for a single property on a particular node will
result in a failed constraint. However, it is allowed to use different operators
for a property, as long as the terms on which these operators are used are different.

Finally, the last `$Term` denotes the value of the property.

!!! warning
    Failing property constraints are ignored (i.e. no error for them is reported).


## Arithmetic Constraints


```statix
$Term $Op $ArithExp $Message?
```

Statix supports several arithmetic constraints. These constraints consist of a
term, an operator and an arithmetic expression. The `$Term` should have type `int`,
while the `$ArithExp` is syntactically guaranteed to have type `int`, given that
all variable references have type `int`.

At the `$Op` position, several comparison operators can be used:

- `#=` asserts that both terms are equal
- `#\\=` asserts that both terms are not equal
- `#>=`{.no-ligatures} asserts that the left term is equal or bigger that the left term
- `#=<` asserts that the left term is equal or smaller that the left term
- `#>` asserts that the left term is strictly bigger that the left term
- `#<` asserts that the left term is strictly smaller that the left term

Arithmetic expressions can be integer literals, variables and bracketed arithmetic
expressions. Variables in an arithmetic expression must have type `int`.
Additionally, the following arithmetic operations can be used:

- `$ArithExp + $ArithExp`: computes integer addition
- `$ArithExp - $ArithExp`: computes integer subtraction
- `$ArithExp * $ArithExp`: computes integer multiplication
- `min($ArithExp, $ArithExp)`: computes the minimum of both arguments
- `max($ArithExp, $ArithExp)`: computes the maximum of both arguments
- `$ArithExp div $ArithExp`: computes the integer divisor (i.e. rounded down
  regular division).
- `$ArithExp mod $ArithExp`: computes the modulus of its arguments.

Unlike other constraints, arithmetic constraint do no inference of values in
the `$ArithExp`. Hence, having any free variables in this expression will cause
the constraint to fail.

!!! note
    As discussed, Statix has a special syntactic category for arithmetic expressions.
    Therefore, arithmetic expressions cannot be used at regular term positions.
    Instead, arithmetic expressions can be embedded in terms using the
    [Arithmetic Expressions](../terms#arithmetic-operations) term syntax.

??? note
    Arithmetic Expressions are implemented using standard Java integers, and hence
    have the same size limitations.


## Messages

```statix
| $Severity $MessageBody $Position?
```

Constraints that might possibly fail can be provided with a customized message.
Such message carry three parameters.

First, the `$Severity` indicates the severity of a message. It may be either
`error`, `warning` or `note`. Note however that warnings and notes can only be
issued for failing [`try`](#try) constraints.

Second, the error message string is provided. This message string may be a regular
[string literal](../terms#strings) or a template literal. Template literals
look as follows:

```statix
$[$ContentPart*]
```

Content parts are either message string literals or interpolated terms. The
escaping rules for string literals in templates are slightly different than for
regular string literals. Message string literals can contain any character,
where square brackets and backslashes must be escaped with a backslash. Just as
regular string literals, tabs, newlines and carriage returns can be encoded with
`\t`, `\n` and `\r`, respectively.

[Terms](../terms) can be inserted in a message template by surrounding them with
(unescaped) square brackets: `[$Term]`. The term may have any type, but must be
well-formed according to the regular typing rules for terms.

!!! bug
    Using functional predicates inside message templates will cause an exception
    when loading the specification.

Thirdly, a position can be assigned to the message:

```statix
@ $Var
```

Here, the `$Var` is assumed to be an AST node. When the constraint on which this
message is placed fails, the message will be shown inline at the AST node pointed
to by this variable.

When no message position is provided, or the assigned position is invalid, Statix
will scan the the arguments to user-defined constraints on the call trace that
led to the failed constraint from left to right for an AST argument, and put the
message on the first valid node found. When no AST node could be found (for
example when the project constraint fails), the error is positioned at the
project resource.

!!! warning
    Messages on projects are often overlooked by users. Hence it is recommended
    that project constraints are designed in a way they can never fail.

When message is provided for a failed constraint, Statix will scan the call
trace for constraints that have a message provided, and use the message it
encounters. If no message is found, a rendering of the failed constraint is used
as a message.
