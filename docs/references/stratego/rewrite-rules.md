# Rewrite Rules

Rewrite rules are used to define basic transformations in Stratego.

## Simple Rewrite Rules

A simple rewrite rule has the form

```stratego
$Label:
  $Term -> $Term
```

It consists of a label that identifies the rule, a left-hand side term, and a right-hand side term.

When a rule is invoked through its label, the current term is match against the left-hand side and replaced with an instantiation of the right-hand side.

A rewrite rule is invoked by applying its label as 

## Conditional Rewrite Rules

```stratego
$Label :
  $Term -> $Term
  where $Strategy
```

## With vs Where


```stratego
$Label :
  $Term -> $Term
  with $Strategy
```


```stratego
$Label :
  $Term -> $Term
  where $Strategy
```

use a where clause when the condition is to determine whether to apply the rule


use a with clause to perform a side computation; has to succeed; will try an exception when it fails

## Combining With and Where

multiple with/where clauses


```stratego
$Label :
  $Term -> $Term
  where $Strategy
  with $Strategy
  with $Strategy
  where $Strategy
```


## Parameterized Rewrite Rules


```stratego
$Label($StrategyArg | $TermArg) :
  $Term -> $Term
  where $Strategy
```

term parameters

strategy parameters


## Typing Rewrite Rules


```
  $Label($StrategyTypes | $TermTypes) :: $Type -> $Type
```
