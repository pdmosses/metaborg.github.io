# Factoring out Traversal

Continuing the inspection of [limitations of term rewriting](../limitations-of-rewriting), we explore how term traversal can be factored out into separate rules.

## Attempt 3: Using Rules for Traversal 

We saw the following definition of the map strategy, which applies a strategy to each element of a list:

```stratego
map(s) : [] -> []
map(s) : [x | xs] -> [<s> x | <map(s)> xs]
```

The definition uses explicit recursive calls to the strategy in the right-hand side of the second rule.
What map does is to traverse the list in order to apply the argument strategy to all elements.
We can use the same technique to other term structures as well.

We will explore the definition of traversals using the propositional formulae, where we introduced the following rewrite rules:

```stratego
module prop-rules
imports libstrategolib prop
rules
  DefI : Impl(x, y)       -> Or(Not(x), y)
  DefE : Eq(x, y)         -> And(Impl(x, y), Impl(y, x))
  DN   : Not(Not(x))      -> x
  DMA  : Not(And(x, y))   -> Or(Not(x), Not(y))
  DMO  : Not(Or(x, y))    -> And(Not(x), Not(y))
  DAOL : And(Or(x, y), z) -> Or(And(x, z), And(y, z))
  DAOR : And(z, Or(x, y)) -> Or(And(z, x), And(z, y))
  DOAL : Or(And(x, y), z) -> And(Or(x, z), Or(y, z))
  DOAR : Or(z, And(x, y)) -> And(Or(z, x), Or(z, y))
```

Above we saw how a functional style of rewriting could be encoded using extra constructors.
In Stratego we can achieve a similar approach by using rule names, instead of extra constructors.
Thus, one way to achieve normalization to disjunctive normal form, is the use of an explicitly programmed traversal, implemented using recursive rules, similarly to the map example above:


```stratego
module prop-dnf4
imports libstrategolib prop-rules
strategies
  main = io-wrap(dnf)
rules
  dnf : True()     ->          True()
  dnf : False()    ->          False()
  dnf : Atom(x)    ->          Atom(x)
  dnf : Not(x)     -> <dnfred> Not (<dnf>x)
  dnf : And(x, y)  -> <dnfred> And (<dnf>x, <dnf>y)
  dnf : Or(x, y)   ->          Or  (<dnf>x, <dnf>y)
  dnf : Impl(x, y) -> <dnfred> Impl(<dnf>x, <dnf>y)
  dnf : Eq(x, y)   -> <dnfred> Eq  (<dnf>x, <dnf>y)
strategies
  dnfred = try(DN <+ (DefI <+ DefE <+ DMA <+ DMO <+ DAOL <+ DAOR); dnf)
```

The `dnf` rules recursively apply themselves to the direct subterms and then apply dnfred to actually apply the rewrite rules.

We can reduce this program by abstracting over the base cases.
Since there is no traversal into `True`, `False`, and `Atom`s, these rules can be be left out.

```stratego
module prop-dnf5
imports libstrategolib prop-rules
strategies
  main = io-wrap(dnf)
rules
  dnft : Not(x)     -> <dnfred> Not (<dnf>x)
  dnft : And(x, y)  -> <dnfred> And (<dnf>x, <dnf>y)
  dnft : Or(x, y)   ->          Or  (<dnf>x, <dnf>y)
  dnft : Impl(x, y) -> <dnfred> Impl(<dnf>x, <dnf>y)
  dnft : Eq(x, y)   -> <dnfred> Eq  (<dnf>x, <dnf>y)
strategies
  dnf    = try(dnft)
  dnfred = try(DN <+ (DefI <+ DefE <+ DMA <+ DMO <+ DAOL <+ DAOR); dnf)
```

The `dnf` strategy is now defined in terms of the `dnft` rules, which implement traversal over the constructors.
By using `try(dnft)`, terms for which no traversal rule has been specified are not transformed.

We can further simplify the definition by observing that the application of `dnfred` does not necessarily have to take place in the right-hand side of the traversal rules.

```stratego
module prop-dnf6
imports libstrategolib prop-rules
strategies
  main = io-wrap(dnf)
rules
  dnft : Not(x)     -> Not (<dnf>x)
  dnft : And(x, y)  -> And (<dnf>x, <dnf>y)
  dnft : Or(x, y)   -> Or  (<dnf>x, <dnf>y)
  dnft : Impl(x, y) -> Impl(<dnf>x, <dnf>y)
  dnft : Eq(x, y)   -> Eq  (<dnf>x, <dnf>y)
strategies
  dnf    = try(dnft); dnfred
  dnfred = try(DN <+ (DefI <+ DefE <+ DMA <+ DMO <+ DAOL <+ DAOR); dnf)
```

In this program `dnf` first calls `dnft` to transform the subterms of the subject term, and then calls `dnfred` to apply the transformation rules (and possibly a recursive invocation of `dnf`).

The program above has two problems.
First, the traversal behavior is mostly uniform, so we would like to specify that more concisely.
We will address that concern below.
Second, the traversal is not reusable, for example, to define a conjunctive normal form transformation.
This last concern can be addressed by factoring out the recursive call to `dnf` and making it a parameter of the traversal rules.

```stratego
module prop-dnf7
imports libstrategolib prop-rules
strategies
  main = io-wrap(dnf)
rules
  proptr(s) : Not(x)     -> Not (<s>x)
  proptr(s) : And(x, y)  -> And (<s>x, <s>y)
  proptr(s) : Or(x, y)   -> Or  (<s>x, <s>y)
  proptr(s) : Impl(x, y) -> Impl(<s>x, <s>y)
  proptr(s) : Eq(x, y)   -> Eq  (<s>x, <s>y)
strategies
  dnf    = try(proptr(dnf)); dnfred
  dnfred = try(DN <+ (DefI <+ DefE <+ DMA <+ DMO <+ DAOL <+ DAOR); dnf)
  cnf    = try(proptr(cnf)); cnfred
  cnfred = try(DN <+ (DefI <+ DefE <+ DMA <+ DMO <+ DOAL <+ DOAR); cnf)
```

Now the traversal rules are reusable and used in two different transformations, by instantiation with a call to the particular strategy in which they are used (`dnf` or `cnf`).

But we can do better, and also make the composition of this strategy reusable.

```stratego
module prop-dnf8
imports libstrategolib prop-rules
strategies
  main = io-wrap(dnf)
rules
  proptr(s) : Not(x)     -> Not (<s>x)
  proptr(s) : And(x, y)  -> And (<s>x, <s>y)
  proptr(s) : Or(x, y)   -> Or  (<s>x, <s>y)
  proptr(s) : Impl(x, y) -> Impl(<s>x, <s>y)
  proptr(s) : Eq(x, y)   -> Eq  (<s>x, <s>y)
strategies
  propbu(s) = try(proptr(propbu(s))); s
strategies
  dnf    = propbu(dnfred)
  dnfred = try(DN <+ (DefI <+ DefE <+ DMA <+ DMO <+ DAOL <+ DAOR); dnf)
  cnf    = propbu(cnfred)
  cnfred = try(DN <+ (DefI <+ DefE <+ DMA <+ DMO <+ DOAL <+ DOAR); cnf)
```

That is, the `propbu(s)` strategy defines a complete bottom-up traversal over proposition terms, applying the strategy `s` to a term after transforming its subterms.
The strategy is completely independent of the `dnf` and `cnf` transformations, which instantiate the strategy using the dnfred and cnfred strategies.

Come to think of it, `dnfred` and `cnfred` are somewhat useless now and can be inlined directly in the instantiation of the `propbu(s)` strategy:

```stratego
module prop-dnf9
imports libstrategolib prop-rules
strategies
  main = io-wrap(dnf)
rules
  proptr(s) : Not(x)     -> Not (<s>x)
  proptr(s) : And(x, y)  -> And (<s>x, <s>y)
  proptr(s) : Or(x, y)   -> Or  (<s>x, <s>y)
  proptr(s) : Impl(x, y) -> Impl(<s>x, <s>y)
  proptr(s) : Eq(x, y)   -> Eq  (<s>x, <s>y)
strategies
  propbu(s) = try(proptr(propbu(s))); s
strategies
  dnf = propbu(try(DN <+ (DefI <+ DefE <+ DMA <+ DMO <+ DAOL <+ DAOR); dnf))
  cnf = propbu(try(DN <+ (DefI <+ DefE <+ DMA <+ DMO <+ DOAL <+ DOAR); cnf))
```

Now we have defined a transformation independent traversal strategy that is specific for proposition terms.
