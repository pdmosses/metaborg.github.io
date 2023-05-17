# Recovery

SDF3 automatically generates permissive grammars for supporting error-recovery parsing[@JongeKVS12].
The permissive grammars contain recovery productions that can be used to recover from syntactic errors.
The recovery productions are either deletions or insertions.
Deletions can skip over an erroneous part of the input.
Insertions recover from a missing part of the input, e.g. a missing closing bracket.

Handwritten recovery rules can be added to tweak the automatically generated permissive grammar by using the `recover` attribute.
For example, the following insertion enables recovery for missing `if` literals:

```
lexical syntax

  "if" =  {recover}
```

The empty right-hand side makes sure that, in recovery mode, the `if` literal can be parsed even when it is not present in the input.

\bibliography