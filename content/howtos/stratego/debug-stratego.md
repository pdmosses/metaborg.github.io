# Debug Stratego Programs

Debugging Stratego programs can be frustrating.
In [strategic programming](../../background/stratego/strategic-rewriting/strategic-rewriting.md) failure is a first-class citizen and the language supports dynamically typed programming.
Thes are useful features for realizing generic and modular programming.
However, this may mean that that errors may show up late in the game.
A program fails much later then where the error occurs.
Often during pretty-printing.
Here we discuss some remedies for finding the problem.

## Signatures

```stratego
signature
  sorts Exp
  constructors
    Add : Exp * Exp -> Exp
```

Define a good signature for your terms.

Ideally define the syntax of your language in a syntax definition in SDF3, and declare all sorts explicitly, and avoid injections.
This will ensure that a signature and matching pretty-printer are generated automatically, as well as a signature for Statix.


## Types

```stratego
translate :: Exp -> List(Instr)
```

Define type signatures for transformations.

Starting with Stratego2, the language supports the definition of [type signatures for transformations](../../references/stratego/types.md/#transformation-types).
This will catch many obvious errors.


## Use With instead of Where

```stratego
translate :
  Add(e1, e2) -> <concat>[instrs1, instrs2, [Add()]]
  with <translate> e1 => instrs1
  with <translate> e2 => instrs2
```

The [with](/references/stratego/rewrite-rules.md/#with-condition) clause expresses that you expect a premisse of a rewrite rule to succeed in all cases.
When this expectation is violated, the rule will throw an exception and display a stack trace, instead of silently failing.


## Define SPT tests

```spt
test translate [[
  1 + 2
]] run translate
```

Define unit tests in the SPT testing language.


## Debug

```stratego
dbg(|"translate/Add: ")
```

In case the measures above fail, use `dbg` to figure out where the error is in your program.
