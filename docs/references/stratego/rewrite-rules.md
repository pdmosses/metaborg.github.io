# Rewrite Rules

```stratego
$Id($StrategyArg, ... | $TermArg, ...) :
  $Term -> $Term
  $Condition*
```

A rewrite rule has a name, zero or more strategy arguments, zero or more term arguments, a left-hand side term pattern, a right-hand side term pattern, and zero or more conditions.

A rewrite rule application `$Id($StrategExp, ... | $Term)` to a subject term binds the strategy and term arguments and matches the term pattern in the left-hand side to the term.
If the pattern match succeeds, the conditions are applied in turn to the subject term, accumulating bindings to term variables.
When all conditions succeed, the right-hand side term pattern is instantiated with the accumulated variable bindings.

When the pattern match to the left-hand side or one of the conditions fails, the rule fails.


## Where Condition

```stratego
where $StrategyExp
```

A `where` condition performs a strategy expression in the context of the rule arguments, the left-hand side bindings, and the previous conditions, possibly binding term variables.

If the strategy expression fails, the enclosing rule fails.
Failure of a `where` clause is expected.
The strategy expression is expected to be discriminating and only succeed in those cases that the rule should be applied.


## With Condition

```stratego
with $StrategyExp
```

A `with` condition performs a strategy expression in the context of the rule arguments, the left-hand side bindings, and the previous conditions, possibly binding term variables.

A `with` condition expresses the expectation that the strategy expression succeeds in all cases.
When a `with` condition fails, this is an indication of a programming error, and the enclosing rule throws a fatal exception, and the program terminates with a stack trace.


## Simple Rewrite Rules

```stratego
$Id:
  $Term -> $Term
  $Condition*
```

A _simple_ (unparameterized) rewrite rule consists of a name that identifies the rule, a left-hand side term pattern, a right-hand side term pattern, and zero or more conditions.

Example

```stratego
DeMorgan :
  Not(And(e1, e2)) -> Or(Not(e1), Not(e2))
```


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
    Consider specificity ordering in the future.


## Parameterized Rewrite Rules

Rewrite rules can be parameterized with transformation strategies and with terms.

Example.
The following rules define reversal of a list with an accumulator:

```stratego
rules
  reverse :: List(a) -> List(a)
  reverse : xs -> <reverse-acc(|[])> xs

  reverse-acc(|List(a)) :: List(a) -> List(a)
  reverse-acc(|xs) : [] -> xs
  reverse-acc(|xs) : [y | ys] -> <reverse-acc(|[y | xs])> ys
```

When leaving out the term parameters, the bar can be left out

```stratego
$Id($StrategyArg) :
  $Term -> $Term
  $Condition*
```

Example.
The `map(s)` strategy applies transformation `s` to each element of a list:

```stratego
map(a -> b) :: List(a) -> List(b)
map(s) : [] -> []
map(s) : [hd | tl] -> [<s>hd | <map(s)> tl]
```

!!! note
    In the absence of a type system, the distinction between strategy arguments and term arguments was made based on the syntactic distinction.
    In a future version of the language, this syntactic distinction may no longer be necessary based on types.


### Desugaring

A conditional rewrite rule can be desugared to a [strategy definition](strategy-definitions.md) using basic [strategy combinators](strategy-combinators.md).

A simple rewrite rule succeeds if the match of the left-hand side succeeds.
Sometimes it is useful to place additional requirements on the application of a rule, or to compute some value for use in the right-hand side of the rule.
This can be achieved with conditional rewrite rules.

A conditional rule `L: p1 -> p2` where `s` is a simple rule extended with an additional computation `s` which should succeed in order for the rule to apply.
The condition can be used to test properties of terms in the left-hand side, or to compute terms to be used in the right-hand side.
The latter is done by binding such new terms to variables used in the right-hand side.

For example, the `EvalPlus` rule in the following session uses a condition to compute the sum of `i` and `j`:

```stratego
EvalPlus:
  Plus(Int(i),Int(j)) -> Int(k)
  where !(i,j); addS; ?k

<EvalPlus>
  Plus(Int("14"),Int("3")) => Int("17")
```

A conditional rule can be desugared similarly to an unconditional rule.
That is, a conditional rule of the form

```stratego
L : p1 -> p2 where s
```

is syntactic sugar for

```stratego
L = ?p1; where(s); !p2
```

Thus, after the match with `p1` succeeds the strategy `s` is applied to the subject term.
Only if the application of `s` succeeds, is the right-hand side `p2` built.
Note that since `s` is applied within a where, the build `!p2` is applied to the original subject term; only variable bindings computed within `s` can be used in `p2`.

As an example, consider the following constant folding rule, which reduces an addition of two integer constants to the constant obtained by computing the addition.

```stratego
EvalPlus :
  Add(Int(i),Int(j)) -> Int(k) where !(i,j); addS; ?k
```

The addition is computed by applying the primitive strategy addS to the pair of integers `(i,j)` and matching the result against the variable `k`, which is then used in the right-hand side.
This rule is desugared to

```stratego
EvalPlus =
  ?Add(Int(i),Int(j)); where(!(i,j); addS; ?k); !Int(k)
```
