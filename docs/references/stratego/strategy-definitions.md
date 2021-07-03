# Strategy Definitions

```stratego
$Id($StrategyArg, ... | $TermArg, ...) =
  $StrategyExp
```

A strategy definition gives a name to a strategy expression, has zero or more strategy arguments, and zero or more term arguments.


## Simple Definitions

A simple strategy definition gaves a name to a [strategy expression](strategy-combinators.md).

```stratego
$Id = s
```

For example, the following definition defines `desugar` as an application of the `innermost` strategy to the rewrite rule(s) `desugar-exp`.

```stratego
strategies
  desugar :: Module -> Module
  desugar = innermost(desugar-exp)
```

## Parameterized Definitions

Just like [rewrite rules](rewrite-rules.md), strategy definitions can be parameterized with strategies and terms.

```stratego
$Id($StrategyArg, ... | $TermArg, ...) :: $Type -> $Type
$Id(s1, ... | t1, ...) = s
```

When a strategy has no term arguments, the bar can be left out:

```stratego
$Id($StrategyArg, ... ) :: $Type -> $Type
$Id(s1, ...) = s
```

Simple strategy definitions are the special case in which a strategy does not have strategy and term arguments.

For example, the following definition defines `topdown(s)` in terms of sequential composition and generic traversal:

```stratego
topdown(TP) :: TP
topdown(s) = s; all(topdown(s))
```


## Extending Definitions

Just like rewrite rules, strategy definitions can have multiple definitions.
In case a strategy expression fails to apply, the next definition is applied.
When definitions are in the same module, definitions are applied in the textual order they are defined in.
When definitions are defined in separate modules, the order is undefined.


## External Definitions

external definitions

libraries

!!! todo
    finish this section on external definitions

## Local Definitions

!!! todo
    finish this section on local definitions
