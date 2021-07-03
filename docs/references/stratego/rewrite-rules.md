# Rewrite Rules

```stratego
$Id($StrategyArg, ... | $TermArg, ...) :
  $Term -> $Term
  $Condition*
```

A rewrite rule has a name, zero or more strategy argumuents, zero or more term arguments, a left-hand side term pattern, a right-hand side term pattern, and zero or more conditions.

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
The strategy expression is expected to be discrimating and only succeed in those cases that the rule should be applied.


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
  reverse           :: List(a) -> List(a)
  reverse(|List(a)) :: List(a) -> List(a)s  
  reverse      : xs -> <reverse(|[])> xs
  reverse(|xs) : [] -> xs
  reverse(|xs) : [y | ys] -> <reverse-acc(|[y | xs])> ys
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
    In a future version of the language, this syntactic distiction may no longer be necessary based on types.
