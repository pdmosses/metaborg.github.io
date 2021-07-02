# Rewrite Rules

Rewrite rules are used to define basic transformations in Stratego.

## Typing Rewrite Rules

As noted in the [type](../terms/types.md) section, rewrite rules can be typed using a signature of the form

```
  $Id($StrategyTypes | $TermTypes) :: $Type -> $Type
```

Not providing a type signature amounts to declaring the rule as having signature

```
  $Id(?|?) :: ? -> ?
```

That is, nothing is known about the term that is transformed or the strategies and terms that are passed.

But do note that the arity of the strategy and term arguments is relevant for identifying the transformation rule that is defined.


## Simple Rewrite Rules

A _simple_ rewrite rule has the form

```stratego
$Id:
  $Term -> $Term
```

It consists of a name that identifies the rule, a left-hand side term pattern, and a right-hand side term pattern.

Applying a rule to a term `t` entails [matching](../terms/patterns.md) `t` against the left-hand side, binding any variables and replacing it with an instantiation of the right-hand side.

For example, the rewrite rule `DeMorgan`

```stratego
DeMorgan :
  Not(And(e1, e2)) -> Or(Not(e1), Not(e2))
```

transforms a negation of a conjunction to a disjunction of negations.
Applying this rule to the term `Not(And(Var(p), Var(q)))` results in a substitution binding `Var(p)` to `e1` and `Var(q)` to `e2`, and the instantiation `Or(Not(Var(p)), Not(Var(q)))` of the right-hand side of the rule.

Note that a rewrite rule defines a _partial computation_.
Only if the pattern match succeeds is the transformation applied.
Such (pattern match) failure is a first-class citizen in Stratego and its effects are discussed with [strategy combinators](../strategies/sequential.md).


## Rules with the Same Name

Multiple rewrite rules may have the same name.
When a (simple) rewrite rule fails to apply to a term, the next rule with the same name is tried.

For examples, the following rules define desugarings of expressions.

```stratego
rules desugar-exp :: Exp -> Exp

  desugar-exp :
    Seq([], e) -> e

  desugar-exp :
    Seq([e], Unit()) -> e

  desugar-exp :
    Seq([e1, e2 | e*], e3) -> Seq([e1], Seq([e2 | e*], e3))

  desugar-exp :
    Seq([Seq(e1*, e1) | e2*], e2) -> Seq([e1*, e1 | e2*], e2)

  desugar-exp :
    Let(dec*, [e1, e2 | e*]) -> Let(dec*, [Seq([e1, e2 | e*], Unit())])
```

When one rule fails to apply, the next rule is tried.
When the left-hand sides are non-overlapping, the order of the rules does not matter.
In case of overlap, the rules are tried in textual order.
When overlapping rules are defined in separate modules, the order is undefined.

!!! note
    We should consider specificity ordering.

## Conditional Rewrite Rules

A _conditional_ rewrite rule checks a condition or performs a side computation before instantiating the right-hand side of the rule.

The basic form of a conditional rewrite rule in Stratego is

```stratego
$Id :
  $Term -> $Term
  where $Strategy
```

where the [strategy expression](../strategies/sequential.md) represents a computation that may fail.
When the condition fails, the expectation is that some other rule will pick up the computation.

For example, the following conditional rewrite rules combine pattern matching with the predicate `is-atom` to select the rule to apply:

```stratego
rules

  rco-atom :: Exp -> (List(Dec) * Exp)

  rco-atom :   
    Let(dec*, [e]) -> (dec*, e)
    where <is-atom> e  

  rco-atom :   
    e -> ([], e)
    where <is-atom> e

  rco-atom :
    e -> ([VarDec(x, Tid("int"), e)], Var(x))
    where <not(is-atom)> e
    where <newname> "tmp" => x
```

When the condition fails, the application of the rule fails (and the next rule is tried if there is one).


## Side Computations with With

Failure is not always expected.
When a condition is used to express a side computation, the expection may be that it should always succeed.
However, due to a programming error (e.g. a missed case), the condition may fail in some cases.
To guard against such programming errors, the `with` condition expresses that the programmer expects a side computation to always succeed.
When a `with` clause fails, the program should fail with an exception (and a stack trace).

```stratego
$Id :
  $Term -> $Term
  with $Strategy
```

For example, a `translate` transformation from expressions to list of (stack machine) instructions may use side computations to recursively apply the transformation.

```stratego
translate :: Exp -> List(Instr)
translate :
  Plus(e1, e2) -> <concat>[instrs1, instrs2, [ADD()]]
  with <translate>e1 => instrs1
  with <translate>e2 => instrs2
```

The recursive applications are not expected to fail.
Therefore a `with` is used.

Thus, use a `where` clause when the condition is to determine whether to apply the rule, and use a `with` clause to perform a side computation, which has to succeed and will trow an exception when it fails.

## Combining With and Where

Rewrite rules can combine multiple with/where clauses in any order.

```stratego
$Id :
  $Term -> $Term
  where $Strategy
  with $Strategy
  with $Strategy
  where $Strategy
```

The only rule is that `with` clauses should always succeed.

For example, the following `explicate-exp` rule defines the translation of an operator expression in a source language to an operator expression in a target language.

```stratego
explicate-exp :: Exp -> CExp
explicate-exp :
  op#(es) -> cop#(atms)
  where <is-operator> op
  with <map(explicate-atom)> es => atms
  with <operator-to-coperator> op => cop
```

The `where` condition tests whether the rule should be applied using the `is-operator` strategy.
(By using [generic term deconstruction](../strategies/type-unifying.md) to obtain the term constructor.)
The `with` premises define side computations.

## Parameterized Rewrite Rules

Rewrite rules can be parameterized with transformation strategies and with terms.
In general, a parameterized rule has the form:

```stratego
$Id($StrategyArg, ... | $TermArg, ...) :
  $Term -> $Term
  where $Strategy
  ...
```

The strategy parameters represent computations that can be applied in the body of the rule.
The term parameters are terms that are evaluated eagerly at the call site.
The (arity of the) parameters of a rule are part of its identity.
That is, rules with the same name, but different numbers of parameters are different.

For example, the following rules define reversal of a list with an accumulator:

```stratego
rules
  reverse           :: List(a) -> List(a)
  reverse(|List(a)) :: List(a) -> List(a)s  
  reverse      : xs -> <reverse(|[])> xs
  reverse(|xs) : [] -> xs
  reverse(|xs) : [y | ys] -> <reverse-acc(|[y | xs])> ys
```

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

The simple rewrite rules are above are the special case in which there are no strategy and term parameters.
In that case, the parentheses can be left out as well.

!!! note
    In the absence of a type system, the distinction between strategy arguments and term arguments was made based on the syntactic distinction.
    In a future version of the language, this syntactic distiction may no longer be necessary based on types.
