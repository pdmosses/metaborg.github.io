# Strategic Rewriting

## Limitations of Term Rewriting

Term rewriting involves exhaustively applying rules to subterms until no more rules apply.
This requires a strategy for selecting the order in which subterms are rewritten.
The innermost strategy applies rules automatically throughout a term from inner to outer terms, starting with the leaves.
The nice thing about term rewriting is that there is no need to define traversals over the syntax tree; the rules express basic transformation steps and the strategy takes care of applying it everywhere.
However, the complete normalization approach of rewriting turns out not to be adequate for program transformation, because rewrite systems for programming languages will often be non-terminating and/or non-confluent.
In general, it is not desirable to apply all rules at the same time or to apply all rules under all circumstances.

The usual solution is [to encode the strategy in the rewrite rules](../limitations-of-rewriting/).
But this intertwines the strategy with the rules, and makes the latter unreusable.



## Programmable Rewriting Strategies

In general, there are two problems with the functional approach to encoding the control over the application of rewrite rules, when comparing it to the original term rewriting approach: traversal overhead and loss of separation of rules and strategies.

In the first place, the functional encoding incurs a large overhead due to the explicit specification of traversal.
In pure term rewriting, the strategy takes care of traversing the term in search of subterms to rewrite.
In the functional approach traversal is spelled out in the definition of the function, requiring the specification of many additional rules.
A traversal rule needs to be defined for each constructor in the signature and for each transformation.
The overhead for transformation systems for real languages can be inferred from the number of constructors for some typical languages:

```
language : constructors
Tiger    : 65
C        : 140
Java     : 140
COBOL    : 300 - 1200
```

In the second place, rewrite rules and the strategy that defines their application are completely intertwined.
Another advantage of pure term rewriting is the separation of the specification of the rules and the strategy that controls their application.
Intertwining these specifications makes it more difficult to understand the specification, since rules cannot be distinguished from the transformation they are part of.
Furthermore, intertwining makes it impossible to reuse the rules in a different transformation.

Stratego introduces the paradigm of programmable rewriting strategies with generic traversals, a unifying solution in which application of rules can be carefully controlled, while incurring minimal traversal overhead and preserving separation of rules and strategies[@VisserBT98].

The following are the design criteria for strategies in Stratego:

- Separation of rules and strategy: Basic transformation rules can be defined separately from the strategy that applies them, such that they can be understood independently.
- Rule selection: A transformation can select the necessary set of rules from a collection (library) of rules.
- Control: A transformation can exercise complete control over the application of rules. This control may be fine-grained or course-grained depending on the application.
- No traversal overhead: Transformations can be defined without overhead for the definition of traversals.
- Reuse of rules: Rules can be reused in different transformations.
Reuse of traversal schemas: Traversal schemas can be defined generically and reused in different transformations.

## Idioms of Strategic Rewriting

We will examine the language constructs that Stratego provides for programming with strategies, starting with the low-level actions of building and matching terms.
To get a feeling for the purpose of these constructs, we first look at a couple of typical idioms of strategic rewriting.

## Cascading Transformations

The basic idiom of program transformation achieved with term rewriting is that of cascading transformations.
Instead of applying a single complex transformation algorithm to a program, a number of small, independent transformations are applied in combination throughout a program or program unit to achieve the desired effect.
Although each individual transformation step achieves little, the cumulative effect can be significant, since each transformation feeds on the results of the ones that came before it.

One common cascading of transformations is accomplished by exhaustively applying rewrite rules to a subject term.
In Stratego the definition of a cascading normalization strategy with respect to rules `R1`, … , `Rn` can be formalized using the innermost strategy that we saw before:

```stratego
simplify = innermost(R1 <+ ... <+ Rn)
```

The argument strategy of innermost is a selection of rules.
By giving different names to rules, we can control the selection used in each transformation.
There can be multiple applications of innermost to different sets of rules, such that different transformations can co-exist in the same module without interference.
Thus, it is now possible to develop a large library of transformation rules that can be called upon when necessary, without having to compose a rewrite system by cutting and pasting.
For example, the following module defines the normalization of proposition formulae to both disjunctive and to conjunctive normal form:

```stratego
module prop-laws
imports prop
rules

  DefI : Impl(x, y) -> Or(Not(x), y)
  DefE : Eq(x, y)   -> And(Impl(x, y), Impl(y, x))

  DN   : Not(Not(x)) -> x

  DMA  : Not(And(x, y)) -> Or(Not(x), Not(y))
  DMO  : Not(Or(x, y))  -> And(Not(x), Not(y))

  DAOL : And(Or(x, y), z) -> Or(And(x, z), And(y, z))
  DAOR : And(z, Or(x, y)) -> Or(And(z, x), And(z, y))

  DOAL : Or(And(x, y), z) -> And(Or(x, z), Or(y, z))
  DOAR : Or(z, And(x, y)) -> And(Or(z, x), Or(z, y))

strategies

  dnf = innermost(DefI <+ DefE <+ DAOL <+ DAOR <+ DN <+ DMA <+ DMO)
  cnf = innermost(DefI <+ DefE <+ DOAL <+ DOAR <+ DN <+ DMA <+ DMO)
```

The rules are named, and for each strategy different selections from the rule set are made.

<!-- The module even defines two main strategies, which allows us to use one module for deriving multiple programs. Using the --main option of strc we declare which strategy to invoke as main strategy in a particular program. Using the -o option we can give a different name to each derived program.

$ strc -i prop-laws.str -la stratego-lib --main main-dnf -o prop-dnf4 -->

## One-pass Traversals

Cascading transformations can be defined with other strategies as well, and these strategies need not be exhaustive, but can be simpler one-pass traversals.
For example, constant folding of Boolean expressions only requires a simple one-pass bottom-up traversal.
This can be achieved using the bottomup strategy according the following scheme:

```stratego
simplify = bottomup(repeat(R1 <+ ... <+ Rn))
```

The bottomup strategy applies its argument strategy to each subterm in a bottom-to-top traversal.
The repeat strategy applies its argument strategy repeatedly to a term.

Module `prop-eval2` defines the evaluation rules for Boolean expressions and a strategy for applying them using this approach:

```stratego
module prop-eval2
imports libstrategolib prop
rules
  Eval : Not(True())      -> False()
  Eval : Not(False())     -> True()
  Eval : And(True(), x)   -> x
  Eval : And(x, True())   -> x
  Eval : And(False(), x)  -> False()
  Eval : And(x, False())  -> False()
  Eval : Or(True(), x)    -> True()
  Eval : Or(x, True())    -> True()
  Eval : Or(False(), x)   -> x
  Eval : Or(x, False())   -> x
  Eval : Impl(True(), x)  -> x
  Eval : Impl(x, True())  -> True()
  Eval : Impl(False(), x) -> True()
  Eval : Impl(x, False()) -> Not(x)
  Eval : Eq(False(), x)   -> Not(x)
  Eval : Eq(x, False())   -> Not(x)
  Eval : Eq(True(), x)    -> x
  Eval : Eq(x, True())    -> x
strategies
  main = io-wrap(eval)
  eval = bottomup(repeat(Eval))
```

The strategy eval applies these rules in a bottom-up traversal over a term, using the `bottomup(s)` strategy.
At each sub-term, the rules are applied repeatedly until no more rule applies using the `repeat(s)` strategy.
This is sufficient for the `Eval` rules, since the rules never construct a term with subterms that can be rewritten.

Another typical example of the use of one-pass traversals is desugaring, that is rewriting language constructs to more basic language constructs.
Simple desugarings can usually be expressed using a single top-to-bottom traversal according to the scheme

```stratego
simplify = topdown(try(R1 <+ ... <+ Rn))
```

The `topdown` strategy applies its argument strategy to a term and then traverses the resulting term.
The try strategy tries to apply its argument strategy once to a term.

Module `prop-desugar` defines a number of desugaring rules for Boolean expressions, defining propositional operators in terms of others.
For example, rule `DefN` defines `Not` in terms of `Impl`, and rule `DefI` defines `Impl` in terms of `Or` and `Not`.
So not all rules should be applied in the same transformation or non-termination would result.

```stratego
module prop-desugar
imports prop libstrategolib

rules

  DefN  : Not(x)     -> Impl(x, False())
  DefI  : Impl(x, y) -> Or(Not(x), y)
  DefE  : Eq(x, y)   -> And(Impl(x, y), Impl(y, x))
  DefO1 : Or(x, y)   -> Impl(Not(x), y)
  DefO2 : Or(x, y)   -> Not(And(Not(x), Not(y)))
  DefA1 : And(x, y)  -> Not(Or(Not(x), Not(y)))
  DefA2 : And(x, y)  -> Not(Impl(x, Not(y)))

  IDefI : Or(Not(x), y) -> Impl(x, y)

  IDefE : And(Impl(x, y), Impl(y, x)) -> Eq(x, y)

strategies

  desugar =
    topdown(try(DefI <+ DefE))

  impl-nf =
    topdown(repeat(DefN <+ DefA2 <+ DefO1 <+ DefE))

  main-desugar =
    io-wrap(desugar)

  main-inf =
    io-wrap(impl-nf)
```

The strategies `desugar` and `impl-nf` define two different desugaring transformation based on these rules.
The desugar strategy gets rid of the implication and equivalence operators, while the `impl-nf` strategy reduces an expression to implicative normal-form, a format in which only implication (`Impl`) and `False()` are used.

A final example of a one-pass traversal is the `downup` strategy, which applies its argument transformation during a traversal on the way down, and again on the way up:

```stratego
simplify = downup(repeat(R1 <+ ... <+ Rn))
```

An application of this strategy is a more efficient implementation of constant folding for Boolean expressions:

```stratego
eval = downup(repeat(Eval))
```

This strategy reduces terms such as


```stratego
And(... big expression ..., False())
```

in one step (to `False()` in this case), while the bottomup strategy defined above would first evaluate the big expression.

## Staged Transformations

Cascading transformations apply a number of rules one after another to an entire tree.
But in some cases this is not appropriate.
For instance, two transformations may be inverses of one another, so that repeatedly applying one and then the other would lead to non-termination.
To remedy this difficulty, Stratego supports the idiom of staged transformation.

In staged computation, transformations are not applied to a subject term all at once, but rather in stages.
In each stage, only rules from some particular subset of the entire set of available rules are applied.
In the TAMPR program transformation system this idiom is called sequence of normal forms, since a program tree is transformed in a sequence of steps, each of which performs a normalization with respect to a specified set of rules.
In Stratego this idiom can be expressed directly according to the following scheme:

```stratego
strategies

  simplify =
      innermost(A1 <+ ... <+ Ak)
    ; innermost(B1 <+ ... <+ Bl)
    ; ...
    ; innermost(C1 <+ ... <+ Cm)
```

## Local Transformations

In conventional program optimization, transformations are applied throughout a program.
In optimizing imperative programs, for example, complex transformations are applied to entire programs.
In GHC-style compilation-by-transformation, small transformation steps are applied throughout programs.
Another style of transformation is a mixture of these ideas. Instead of applying a complex transformation algorithm to a program we use staged, cascading transformations to accumulate small transformation steps for large effect.
However, instead of applying transformations throughout the subject program, we often wish to apply them locally, i.e., only to selected parts of the subject program.
This allows us to use transformations rules that would not be beneficial if applied everywhere.

One example of a strategy which achieves such a transformation is


```stratego
strategies

  transformation =
    alltd(
      trigger-transformation
      ; innermost(A1 <+ ... <+ An)
    )
```

The strategy `alltd(s)` descends into a term until a subterm is encountered for which the transformation s succeeds.
In this case the strategy trigger-transformation recognizes a program fragment that should be transformed.
Thus, cascading transformations are applied locally to terms for which the transformation is triggered.
Of course more sophisticated strategies can be used for finding application locations, as well as for applying the rules locally.
Nevertheless, the key observation underlying this idiom remains: Because the transformations to be applied are local, special knowledge about the subject program at the point of application can be used.
This allows the application of rules that would not be otherwise applicable.

## References

\bibliography
