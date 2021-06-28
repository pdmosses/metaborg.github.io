# Rewrite Rules

Rewrite rules are used to define basic transformations in Stratego.

## Simple Rewrite Rules

A _simple_ rewrite rule has the form

```stratego
$Id:
  $Term -> $Term
```

It consists of a name that identifies the rule, a left-hand side term pattern, and a right-hand side term pattern.

Applying a rule to a term `t` entails [matching](../patterns/) `t` against the left-hand side, binding any variables and replacing it with an instantiation of the right-hand side.

For example, the rewrite rule `DeMorgan`

```stratego
DeMorgan : Not(And(e1, e2)) -> Or(Not(e1), Not(e2))
```

transforms a negation of a conjunction to a disjunction of negations.
Applying this rule to the term `Not(And(Var(p), Var(q)))` results in a substitution binding `Var(p)` to `e1` and `Var(q)` to `e2`, and the instantiation `Or(Not(Var(p)), Not(Var(q)))` of the right-hand side of the rule.

Note that a rewrite rule defines a _partial computation_.
Only if the pattern match succeeds is the transformation applied.
Such (pattern match) failure is a first-class citizen in Stratego and its effects are discussed with [strategy combinators](../strategy-combinators/).

## Conditional Rewrite Rules

A _conditional_ rewrite rule checks a condition or performs a side computation before instantiating the right-hand side of the rule.

The basic form of a conditional rewrite rule in Stratego is

```stratego
$Id :
  $Term -> $Term
  where $Strategy
```

where the [strategy expression](../strategy-combinators/) represents a computation that may fail.
When the condition fails, the expectation is that some other rule will pick up the computation.

For example, the conditional rewrite rule

```stratego
  foo :
    e -> term
    where <is(string)> e
```

!!! todo
    come up with a sensible example

When the condition fails, the application of the rule fails in the sense above.


## Side Computations with With

Failure is not always expected.
When a condition is used to express a side computation, the expection may be that it should always succeed.
However, due to a programming error (e.g. a missed case), the condition may fail in some cases.
To guard agains such cases the `with` condition expresses that the programmer expects a side computation to always succeed.
When this fails, the program should fail with an exception (and a stack trace).

```stratego
$Id :
  $Term -> $Term
  with $Strategy
```


```stratego
translate :
  Plus(e1, e2) -> <concat>[instrs1, instrs2, [ADD()]]
  with <translate>e1 => instrs1
  with <translate>e2 => instrs2
```

use a where clause when the condition is to determine whether to apply the rule


use a with clause to perform a side computation; has to succeed; will try an exception when it fails

## Combining With and Where

multiple with/where clauses


```stratego
$Id :
  $Term -> $Term
  where $Strategy
  with $Strategy
  with $Strategy
  where $Strategy
```

For example, the following `explicate-exp` rule defines the translation of an operator expression in one language to an operator expression in a different language.

```stratego
explicate-exp :
  op#(es) -> cop#(atms)
  where <is-operator> op
  with <map(explicate-atom)> es => atms
  with <operator-to-coperator> op => cop
```

The `where` condition tests whether the rule should be applied using the `is-operator` strategy.
(By using generic term deconstruction to obtain the term constructor.)
The `with` premises define side computations.

## Parameterized Rewrite Rules


```stratego
$Id($StrategyArg | $TermArg) :
  $Term -> $Term
  where $Strategy
```

term parameters

strategy parameters

When leaving out the term parameters, the bar can be left out as well

```stratego
$Id($StrategyArg) :
  $Term -> $Term
  where $Strategy
```

For example, the `map(s)` strategy applies transformation `s` to each element of a list:

```stratego
map(a -> b) :: List(a) -> List(b)
map(s) : [] -> []
map(s) : [hd | tl] -> [<s>hd | <map(s)> tl]
```

!!! note
    In the absence of a type system, the distinction between strategy arguments and term arguments was maded based on the syntactic distinction.
    In a future version of the language, this syntactic distiction may no longer be necessary based on types.


## Typing Rewrite Rules

As noted in the [type](../types/) section, rewrite rules can be typed using a signature of the form

```
  $Id($StrategyTypes | $TermTypes) :: $Type -> $Type
```

Not providing a type signature amounts to declaring the rule as having signature

```
  $Id(?|?) :: ? -> ?
```

That is, nothing is known about the term that is transformed or the strategies and terms that are passed.

But do note that the arity of the strategy and term arguments is relevant for identifying the transformation rule that is defined.
