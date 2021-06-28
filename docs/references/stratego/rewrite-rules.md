# Rewrite Rules

## Simple Rewrite Rules

```stratego
$Label:
  $Term -> $Term
```


## Conditional Rewrite Rules

```stratego
$Label :
  $Term -> $Term
  where $Strategy
```



## With vs Where

use a where clause when the condition is to determine whether to apply the rule


use a with clause to perform a side computation; has to succeed; will try an exception when it fails

## Combining With and Where

multiple with/where clauses


## Parameterized Rewrite Rules


term parameters

strategy parameters
