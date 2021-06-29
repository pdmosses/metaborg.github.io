# Rules

User-defined constraints and their rules make up the main part of a Statix specification.
In this section, we describe the definition and usage of user-defined constraints
and their rules.

## Constraint Definitions

In order to define a custom constraint, its type must be declared first. A
constraint can be declared in a `rules` section, or in a `constraints` subsection
of a `signature` section.

A constraint is declared by specifying its name and argument type. For more
information on types, please refer to the [Types](../types) section. Note that
the name of the constraint must be unique within a specification.

```statix
$ConstraintName : {$Type "*"}*
```

!!! note
    In this reference manual, we consistently use the term 'constraint declaration'
    for the introduction of new user-defined constraints. However, in practise,
    these are sometimes also referred to as 'predicate' or just simply 'constraint'.

When a constraint declaration is provided this way, it can be used as a constraint
by providing concrete arguments, separated by comma's.

```statix
$ConstraintName({$Term ","}*)
```

The sorts of the argument terms should be equal to the sorts in the constraint
declaration.


## Rule Definitions

When solving a user-defined constraint, a rule for that constraint is unfolded
in order to infer a model satisfying the constraint.

```statix
[$RuleName]$ConstraintName({$Pattern ","}*) :- $Constraint.
```

The part _before_ the turnstile (`:-`) is often referred to as the _head_ of the
rule, while the `$Constraint` after the turnstile is denoted as _body_. When
applying a rule, each head pattern (which is just a term) will be matched with
its corresponding actual argument.

Statically, the sorts of the terms in `$Patterns` are type-checked based on the
constraint declaration. Any variables in patterns are implicitly introduced in
the scope of the rule. Patterns can be non-linear. That is, a variable may occur
multiple times in a pattern. Operationally, the subterms at these positions are
then required to be structurally equal.

Note that multiple rules for a single constraint can, and often will, be provided.
For each constraint, the rule that is used for simplification is determined by
the _guard_ of the rule. This guard is derived from the head pattern: a rule
can only be applied when the constraint arguments match the patterns.

During constraint solving, Statix will try at most one rule for each constraint.
The appropriate rule is selected by applying the following heuristics in order:
1. Rules with a smaller domain are preferred over rules with a larger domain.
2. When pairwise comparing rules, the rule for which, in left-to-right order, a
   more specific pattern is encountered first is preferred over the other.
For all cases where these heuristics do not decide which rule to use for a
constraint, compile time "Overlapping patterns" errors will be emitted.

The `$RuleName` is just a name that can be used for documentation purposes.
It cannot be referenced from any position in the specification, and may be
omitted altogether.


## Axiom rules

In some cases, a constraint trivially holds for particular inputs. For such
constraints, an _axiom rule_ can be specified.

```statix
[$RuleName]$ConstraintName({$Pattern ","}*).
```

This rule is similar to a regular rule, but lacks a body. When applying such a
rule, no new constraints are introduced, reflecting the fact that the constraint
trivially holds for these arguments.


## Functional Rules

Some user-defined constraints can be thought of more naturally as a function:
a constraint where a particular term is inferred by the constraint, rather than
validated. Statix allows to write constraints in a functional idiom as follows:

First, a constraint declaration for such 'functional constraints' must be provided
as follows:

```statix
$ConstraintName : {$Type "*"}* -> $Type
```

In addition to the regular list of input sorts, a sort for the output term is
provided to the constraint declaration.

Rule definitions for a functional constraint look as follows:

```statix
[$RuleName]$ConstraintName({$Pattern ","}*) = $Term :- $Constraint.
```

Compared to predicative rule definitions as introduced earlier in this section,
an additional term after an equality-sign is appended to the rule head. This
term denotes the output term (the term inferred by the rule).

A functional constraint can be used in a [_term_](../terms) position, as opposed
to a [_constraint_](../basic-constraints) position for predicative rules.
Otherwise, their syntax is the same.

```statix
$ConstraintName({$Term ","}*)
```

Semantically, the output term of applying the constraint is substituted at the
position of the application of the functional predicate.

!!! note
    When we want to make the distinction between these two forms of constraints
    explicit, we usually refer to either groups with 'predicative constraint
    declarations' and 'predicative constraints', versus 'functional constraint
    declarations' and 'functional constraints', respectively.


## Mapping rules


## Injections of namespaces, relations and constraints


## Example

```statix
module rules-example

signature
  constraints
    lub: TYPE * TYPE * TYPE

rules

  typeOfExp: Exp -> TYPE

  typeOfExp(Cons(hd, tl)) = LIST(T) :- {Th Ttl}
    typeOfExp(hd) == Th,
    typeOfExp(tl) == LIST(Ttl),
    lub(Th, Ttl, T).

  typeOfExp(Nil()) = LIST(_).

```
