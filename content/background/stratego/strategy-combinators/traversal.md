# Traversal Combinators

There are many ways to traverse a tree.
For example, a bottom-up traversal, visits the subterms of a node before it visits the node itself, while a top-down traversal visits nodes before it visits children.
One-pass traversals traverse the tree one time, while fixed-point traversals, such as innermost, repeatedly traverse a term until a normal form is reached.

Rather than provide built-in implementations for all traversals needed in transformations, Stratego defines traversals in terms of the primitive ingredients of traversal.
For example, a top-down, one-pass traversal strategy will first visit a node, and then descend to the children of a node in order to recursively traverse all subterms.
Similarly, the bottom-up, fixed-point traversal strategy innermost, will first descend to the children of a node in order to recursively traverse all subterms, then visit the node itself, and possibly recursively reapply the strategy.

Traversal in Stratego is based on the observation[@LuttikV97] that a full term traversal is a recursive closure of a one-step descent, that is, an operation that applies a strategy to one or more direct subterms of the subject term.
By separating this one-step descent operator from recursion, and making it a first-class operation, many different traversals can be defined.

Here we explore the ways in which Stratego supports the definition of traversal strategies.
We start with explicitly programmed traversals using recursive traversal rules. Next, congruences operators provide a more concise notation for such data-type specific traversal rules.
Finally, generic traversal operators support data type independent definitions of traversals, which can be reused for any data type.
Given these basic mechanisms, we conclude with an exploration of idioms for traversal and standard traversal strategies in the Stratego Library.


## Congruence Operators

Congruence operators provide a convenient abbreviation of [traversal with rewrite rules](../../../background/stratego/strategic-rewriting/traversal-with-rules.md).
A congruence operator applies a strategy to each direct subterm of a specific constructor.
For each n-ary constructor `c` declared in a signature, there is a corresponding congruence operator `c(s1 , ..., sn)`, which applies to terms of the form `c(t1 , ..., tn)` by applying the argument strategies to the corresponding argument terms.
A congruence fails if the application of one the argument strategies fails or if constructor of the operator and that of the term do not match.

For example, consider the following signature of expressions:

```stratego
module expressions
signature
  sorts Exp
  constructors
    Int   : String -> Exp
    Var   : String -> Exp
    Plus  : Exp * Exp -> Exp
    Times : Exp * Exp -> Exp
```

The following applications apply the congruence operators `Plus` and `Times` to a term:

```stratego
<Plus(!Var("a"), id)> Plus(Int("14"),Int("3")) => Plus(Var("a"),Int("3"))

<Times(id, !Int("42"))> Plus(Var("a"),Int("3")) // fails
```

The first application shows how a congruence transforms a specific subterm, that is the strategy applied can be different for each subterm.
The second application shows that a congruence only succeeds for terms constructed with the same constructor.

<!-- The import at the start of the session is necessary to declare the constructors used; the definitions of congruences are derived from constructor declarations.
Forgetting this import would lead to a complaint about an undeclared operator:

```stratego
stratego> !Plus(Int("14"),Int("3"))
Plus(Int("14"),Int("3"))
stratego> Plus(!Var("a"), id)
operator Plus/(2,0) not defined
command failed
```
-->

## Defining Traversals with Congruences

Since congruence operators define a one-step traversal for a specific constructor, they capture the pattern of [traversal rules](../../../background/stratego/strategic-rewriting/traversal-with-rules.md).
That is, a traversal rule such as

```stratego
proptr(s) : And(x, y) -> And(<s>x, <s>y)
```

can be written by the congruence `And(s,s)`.
Applying this to the `prop-dnf` program we can replace the traversal rules by congruences as follows:

```stratego
module prop-dnf10
imports prop-rules
strategies
  proptr(s) = Not(s) <+ And(s, s) <+ Or(s, s) <+ Impl(s, s) <+ Eq(s, s)
  propbu(s) = try(proptr(propbu(s))); s
strategies
  dnf = propbu(try(DN <+ (DefI <+ DefE <+ DMA <+ DMO <+ DAOL <+ DAOR); dnf))
  cnf = propbu(try(DN <+ (DefI <+ DefE <+ DMA <+ DMO <+ DOAL <+ DOAR); cnf))
```

<!-- Observe how the five traversal rules have been reduced to five congruences which fit on a single line. -->


## Traversing Tuples and Lists

Congruences can also be applied to tuples, `(s1,s2,...,sn)`, and lists, `[s1,s2,...,sn]`.
A special list congruence is `[]` which ‘visits’ the empty list.
As an example, consider again the definition of `map(s)` using recursive traversal rules:

```stratego
map(s) : [] -> []
map(s) : [x | xs] -> [<s> x | <map(s)> xs]
```

Using list congruences we can define this strategy as:

```stratego
map(s) = [] <+ [s | map(s)]
```

The `[]` congruence matches an empty list.
The `[s | map(s)]` congruence matches a non-empty list, and applies `s` to the head of the list and `map(s)` to the tail.
Thus, `map(s)` applies `s` to each element of a list:

```stratego
<map(inc)> [1,2,3] => [2,3,4]
```

Note that `map(s)` only succeeds if `s` succeeds for each element of the list.
The `fetch` and `filter` strategies are variations on map that use the failure of `s` to list elements.

```stratego
fetch(s) = [s | id] <+ [id | fetch(s)]
```

The `fetch` strategy traverses a list until it finds a element for which `s` succeeds and then stops.
That element is the only one that is transformed.

```stratego
filter(s) = [] + ([s | filter(s)] <+ ?[ |<id>]; filter(s))
```

The `filter` strategy applies `s` to each element of a list, but only keeps the elements for which it succeeds.

```stratego
even = where(<eq>(<mod>(<id>,2),0))

<filter(even)> [1,2,3,4,5,6,7,8] => [2,4,6,8]
```


## Format Checking

Another application of congruences is in the definition of format checkers.
A format checker describes a subset of a term language using a recursive pattern.
This can be used to verify input or output of a transformation, and for documentation purposes.
Format checkers defined with congruences can check subsets of signatures or regular tree grammars.
For example, the subset of terms of a signature in a some normal form.

As an example, consider checking the output of the `dnf` and `cnf` transformations.

```stratego
conj(s) = And(conj(s), conj(s)) <+ s
disj(s) = Or (disj(s), disj(s)) <+ s

// Conjunctive normal form
conj-nf = conj(disj(Not(Atom(id)) <+ Atom(id)))

// Disjunctive normal form
disj-nf = disj(conj(Not(Atom(id)) <+ Atom(id)))
```

The strategies `conj(s)` and `disj(s)` check that the subject term is a conjunct or a disjunct, respectively, with terms satisfying s at the leaves.
The strategies `conj-nf` and `disj-nf` check that the subject term is in conjunctive or disjunctive normal form, respectively.


## Generic Traversal

Using congruence operators we constructed a generic, i.e. transformation independent, bottom-up traversal for proposition terms.
The same can be done for other data types.
However, since the sets of constructors of abstract syntax trees of typical programming languages can be quite large, this may still amount to quite a bit of work that is not reusable across data types; even though a strategy such as bottom-up traversal, is basically data-type independent.
Thus, Stratego provides generic traversal by means of several generic one-step descent operators.
The operator `all`, applies a strategy to all direct subterms.
The operator `one`, applies a strategy to one direct subterm, and the operator `some`, applies a strategy to as many direct subterms as possible, and at least one.


## Visiting All Subterms

The `all(s)` strategy transforms a constructor application by applying the parameter strategy `s` to each direct subterm.
An application of `all(s)` fails if the application to one of the subterms fails.
The following example shows how all (1) applies to any term, and (2) applies its argument strategy uniformly to all direct subterms.
That is, it is not possible to do something special for a particular subterm (that’s what congruences are for).


```stratego
<all(!Var("a"))>
  Plus(Int("14"), Int("3")) => Plus(Var("a"), Var("a"))

<all(!Var("z"))>
  Times(Var("b"), Int("3")) => Times(Var("z"), Var("z"))
```


## Defining Traversals with All

The `all(s)` operator is really the ultimate replacement for the [traversal with rules](../../../background/stratego/strategic-rewriting/traversal-with-rules.md) idiom.
Instead of specifying a rule or congruence for each constructor, the single application of the `all` operator takes care of traversing all constructors.
Thus, we can replace the `propbu` strategy by a completely generic definition of bottom-up traversal.
Consider again the last definition of `propbu`:

```stratego
proptr(s) = Not(s) <+ And(s, s) <+ Or(s, s) <+ Impl(s, s) <+ Eq(s, s)
propbu(s) = try(proptr(propbu(s))); s
```

The role of `proptr(s)` in this definition can be replaced by `all(s)`, since that achieves exactly the same, namely applying `s` to the direct subterms of constructors:

```stratego
propbu(s) = all(propbu(s)); s
```

Moreover, `all` succeeds on any constructor in any signature, so we can also drop the `try` as well, which was there only because `proptr` fails on the ``Atom(...)``, `True()`, and `False()` nodes at the leaves.

However, the strategy now is completely generic, i.e. independent of the particular structure it is applied to.
In the Stratego Library this strategy is called `bottomup(s)`, and defined as follows:

```stratego
bottomup(s) = all(bottomup(s)); s
```

It first recursively transforms the subterms of the subject term and then applies `s` to the result.
Using this definition, the normalization of propositions now reduces to the following module, which is only concerned with the selection and composition of rewrite rules:

```stratego
module prop-dnf11
imports prop-rules
strategies
  dnf = bottomup(try(DN <+ (DefI <+ DefE <+ DMA <+ DMO <+ DAOL <+ DAOR); dnf))
  cnf = bottomup(try(DN <+ (DefI <+ DefE <+ DMA <+ DMO <+ DOAL <+ DOAR); cnf))
```

In fact, these definitions still contain a reusable pattern.
With a little squinting we see that the definitions match the following pattern:

```stratego
dnf = bottomup(try(dnf-rules; dnf))
cnf = bottomup(try(cnf-rules; cnf))
```

In which we can recognize the definition of innermost reduction, which the Stratego Library defines as:

```stratego
innermost(s) = bottomup(try(s; innermost(s)))
```

The `innermost` strategy performs a bottom-up traversal of a term.
After transforming the subterms of a term it tries to apply the transformation `s`.
If successful the result is recursively transformed with an application of `innermost`.
This brings us to the final form for the proposition normalizations:

```stratego
module prop-dnf12
imports prop-rules
strategies
  dnf = innermost(DN <+ DefI <+ DefE <+ DMA <+ DMO <+ DAOL <+ DAOR)
  cnf = innermost(DN <+ DefI <+ DefE <+ DMA <+ DMO <+ DOAL <+ DOAR)
```

Different transformations can be achieved by using a selection of rules and a strategy, which is generic, yet defined in Stratego itself using strategy combinators.


## Visiting One Subterm

The `one(s)` strategy transforms a constructor application by applying the parameter strategy `s` to exactly one direct subterm.
An application of `one(s)` fails if the application to all of the subterms fails.
The following applications illustrate the behavior of the combinator:

```stratego
<one(!Var("a"))>
  Plus(Int("14"), Int("3")) => Plus(Var("a"), Int("3"))

<one(\ Int(x) -> Int(<addS>(x,"1")) \ )>
  Plus(Var("a"), Int("3")) => Plus(Var("a"), Int("4"))

<one(?Plus(_,_))>
  Plus(Var("a"), Int("4")) // fails
```


## Defining Traversals with One

A frequently used application of `one` is the `oncetd(s)` traversal, which performs a left to right depth first search/transformation that stops as soon as s has been successfully applied.

```stratego
oncetd(s) = s <+ one(oncetd(s))
```

Thus, `s` is first applied to the root of the subject term.
If that fails, its direct subterms are searched one by one (from left to right), with a recursive call to `oncetd(s)`.

An application of `oncetd` is the `contains(|t)` strategy, which checks whether the subject term contains a subterm that is equal to t.

```stratego
contains(|t) = oncetd(?t)
```

Through the depth first search of `oncetd`, either an occurrence of `t` is found, or all subterms are verified to be unequal to `t`.

Here are some other one-pass traversals using the one combinator:

```stratego
oncebu(s)  = one(oncebu(s)) <+ s
spinetd(s) = s; try(one(spinetd(s)))
spinebu(s) = try(one(spinebu(s))); s
```

Here are some fixe-point traversals, i.e., traversals that apply their argument transformation exhaustively to the subject term.

```stratego
reduce(s)     = repeat(rec x(one(x) + s))
outermost(s)  = repeat(oncetd(s))
innermostI(s) = repeat(oncebu(s))
```

The difference is the subterm selection strategy.


## Visiting Some Subterms

The `some(s)` strategy transforms a constructor application by applying the parameter strategy `s` to as many direct subterms as possible and at least one. An application of `some(s)` fails if the application to all of the subterms fails.

Some one-pass traversals based on some:

```stratego
sometd(s) = s <+ some(sometd(s))
somebu(s) = some(somebu(s)) <+ s
```

A fixed-point traversal with some:

```stratego
reduce-par(s) = repeat(rec x(some(x) + s))
```


## References

\bibliography
