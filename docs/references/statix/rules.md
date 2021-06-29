# Rules

User-defined constraints and their rules make up the main part of a Statix specification.
In this section, we describe the definition and usage of user-defined constraints
and their rules.

## Constraint Definitions

In order to define a custom constraint, its type must be declared first. A
constraint can be declared in a `rules` section, or in a `constraints` subsection
of a `signature` section.

A constraint is declared by specifying its name and argument type. For more
information on types, please refer to the [Terms](../terms) section. Note that
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

!!! info
    Every specification with functional predicates is normalized to a form with
    only regular predicates. To show the normal form of a specification in
    Eclipse, use the `Spoofax > Syntax > Format normalized AST` menu action.

## Mapping rules

Another common pattern in Statix is defining a predicate that instantiates a
predicate for all elements in a list. Statix allows derive such mapping rules
using the `maps` keyword as follows:

```statix
$MappingConstraintName maps $MappedConstraintName({$Lift ","})
```

A lift specifier (`$Lift`) can be one of the following:

- `*`: The *identity lift*. This lift specifier indicates that this argument is
  passed to the mapped constraint unchanged.
- `list(*)`: The *list lift*: This lift specifier indicates that the mapped
  constraint will be instantiated for each element in the list at that argument
  position. Each constraint defined with `maps`, must contain at least one list
  lift. Otherwise, the mapping would be a no-op.
- `({$Lift ","}+)`: The *tuple lift*: This lift specifier indicates that arguments
  are extracted from a tuple. For each tuple argument, a corresponding lifting
  is applied afterwards.

The type of `$MappingConstraintName` is inferred by inverse application of the
lift specifiers to the type of `$MappedConstraintName`. Therefore, no explicit
declaration of the type of the mapping constraint is required.

Similar to predicative constraints, functional mapping constraints can be derived:

```statix
$MappingConstraintName maps $MappedConstraintName({$Lift ","}) = $Lift
```

In addition to lift specifiers of the input arguments, a lift specifier for the
inferred term must be provided as well. This lift specifier indicates how the
inferred terms from the mapped constraints are aggregated and returned by the
mapping constraint.

_Example._ A common example where mapping rules are used is when type-checking a
list of declarations. A specification snippet for that could look as follows:

```statix
rules

  declOk: scope * Decl
  declsOk maps declOk(*, list(*))

  // rules for declOk
```

In this snippet, the `declsOk` constraint instantiates `declOk` for each
declaration in a list of declaration. Its inferred type is `scope * list(Decl)`.

When mapping functional constraints, a lift specifier for the inferred term
must be provided as well. This lift specifier indicates how the inferred values
of the mapped constraint are returned by the mapping constraint.

When using multiple list lifts in the input, the resulting constraint will zip
the arguments. This implicitly requires the input lists to be of equal length.
The creation of a cartesian product can be achieved by repeated application of
the `maps` construct for each argument.

!!! info
    Similar to functional constraints, constraints derived using the `maps`
    construct are normalized to regular predicative constraints. This normalization
    can be inspected using the `Spoofax > Syntax > Format normalized AST` menu action.

## Injections of Namespaces and Relations

For convenience, it is possible to declare namespaces, namespace queries (both
deprecated) and relations in a `rules` section as well.

```statix
rules

  namespace Var: string
  resolve Var
    filter P* I*

  relation var: string -> TYPE

```
