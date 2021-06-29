# Term Rewriting

In term rewriting a term is transformed by repeated application of rewrite rules.
To see how this works we take as example the language of propositional formulae, also known as Boolean expressions:

```stratego
module prop
signature
  sorts Prop
  constructors
    False : Prop
    True  : Prop
    Atom  : String -> Prop
    Not   : Prop -> Prop
    And   : Prop * Prop -> Prop
    Or    : Prop * Prop -> Prop
    Impl  : Prop * Prop -> Prop
    Eq    : Prop * Prop -> Prop
```

Given this signature we can write terms such as `And(Impl(True(),False()),False())`, and `And(Atom("p"),False()))`.
Atoms are also known as proposition letters; they are the variables in propositional formulae.
That is, the truth value of an atom should be provided in order to fully evaluate an expression.
Here we will evaluate expressions as far as possible, a transformation also known as constant folding.
We will do this using rewrite rules that define how to simplify a single operator application.

## Term Patterns

A term pattern is a term with meta variables, which are identifiers that are not declared as (nullary) constructors.
For example, `And(x, True())` is a term pattern with variable `x`.
Variables in term patterns are sometimes called meta variables, to distinguish them from variables in the source language being processed.
For example, while atoms in the proposition expressions are variables from the point of view of the language, they are not variables from the perspective of a Stratego program.

A term pattern `p` matches with a term `t`, if there is a substitution that replaces the variables in `p` such that it becomes equal to `t`.
For example, the pattern `And(x, True())` matches the term `And(Impl(True(),Atom("p")),True())` because replacing the variable `x` in the pattern by `Impl(True(),Atom("p"))` makes the pattern equal to the term.
Note that `And(Atom("x"),True())` does not match the term `And(Impl(True(),Atom("p")),True())`, since the subterms `Atom("x")` and `Impl(True(),Atom("p"))` do not match.

## Rewrite Rules

An unconditional rewrite rule has the form `L : p1 -> p2`, where `L` is the name of the rule, `p1` is the left-hand side and `p2` the right-hand side term pattern.
A rewrite rule `L : p1 -> p2` applies to a term `t` when the pattern `p1` matches `t`.
The result is the instantiation of `p2` with the variable bindings found during matching.
For example, the rewrite rule

```stratego
E : Eq(x, False()) -> Not(x)
```

rewrites the term `Eq(Atom("q"),False())` to `Not(Atom("q"))`, since the variable `x` is bound to the subterm `Atom("q")`.

## Evaluation Rules

Now we can create similar evaluation rules for all constructors of sort `Prop`:

```stratego
module prop-eval-rules
imports prop
rules
  E : Not(True())      -> False()
  E : Not(False())     -> True()
  E : And(True(), x)   -> x
  E : And(x, True())   -> x
  E : And(False(), x)  -> False()
  E : And(x, False())  -> False()
  E : Or(True(), x)    -> True()
  E : Or(x, True())    -> True()
  E : Or(False(), x)   -> x
  E : Or(x, False())   -> x
  E : Impl(True(), x)  -> x
  E : Impl(x, True())  -> True()
  E : Impl(False(), x) -> True()
  E : Impl(x, False()) -> Not(x)
  E : Eq(False(), x)   -> Not(x)
  E : Eq(x, False())   -> Not(x)
  E : Eq(True(), x)    -> x
  E : Eq(x, True())    -> x
strategies
  eval = innermost(E)
```

Note that all rules have the same name, which is allowed in Stratego.

<!-- Next we want to normalize terms with respect to a collection of rewrite rules.
This entails applying all rules to all subterms until no more rules can be applied.
The following module defines a rewrite system based on the rules for propositions above:

```stratego
module prop-eval
imports prop-eval-rules
strategies
  eval = innermost(E)
```

The module imports the Stratego Library (`libstrategolib`) and the module with the evaluation rules, and then
The module defines the main strategy to apply `innermost(E)` to the input term.
The innermost strategy from the library exhaustively applies its argument transformation to the term it is applied to, starting with inner subterms.

-->

The module defines the `eval` strategy to apply `innermost(E)` to the input term.
The innermost strategy from the library exhaustively applies its argument transformation to the term it is applied to, starting with inner subterms.

As an aside, we have now seen Stratego modules with rules and strategies sections.
It is worth noting that a module can have any number of sections of either type, and that there is no actual semantic difference between the two section headings.
In fact, either rewrite rules and/or strategy definitions can occur in either kind of section.
Nevertheless, it often helps with making your transformations clearer to generally segregate rules and strategy definitions, and so both headings are allowed so you can punctuate your Stratego modules with them to improve readability.

The next commands apply the eval strategy to various terms.

```stratego
<eval> And(Impl(True(),And(False,True)),True) => False

<eval> And(Impl(True,And(Atom("p"),Atom("q"))),Atom("p"))
    => And(And(Atom("p"),Atom("q")),Atom("p"))
```


## Adding Rules to a Rewrite System

Next we extend the rewrite rules above to rewrite a Boolean expression to disjunctive normal form.
A Boolean expression is in disjunctive normal form if it conforms to the following signature:

```stratego
signature
  sorts Or And NAtom Atom
  constructors
    Or   : Or * Or -> Or
         : And -> Or
    And  : And * And -> And
         : NAtom -> And
    Not  : Atom -> NAtom
         : Atom -> NAtom
    Atom : String -> Atom
```

We use this signature only to describe what a disjunctive normal form is, not in an the actual Stratego program.
This is not necessary, since terms conforming to the DNF signature are also Prop terms as defined before.
For example, the disjunctive normal form of

```stratego
And(Impl(Atom("r"),And(Atom("p"),Atom("q"))),Atom("p"))
```

is

```stratego
Or(And(Not(Atom("r")),Atom("p")),
   And(And(Atom("p"),Atom("q")),Atom("p")))
```

Module `prop-dnf-rules` extends the rules defined in prop-eval-rules with rules to achieve disjunctive normal forms:

```stratego
module prop-dnf-rules
imports prop-eval-rules
rules
  E : Impl(x, y) -> Or(Not(x), y)
  E : Eq(x, y)   -> And(Impl(x, y), Impl(y, x))

  E : Not(Not(x)) -> x

  E : Not(And(x, y)) -> Or(Not(x), Not(y))
  E : Not(Or(x, y))  -> And(Not(x), Not(y))

  E : And(Or(x, y), z) -> Or(And(x, z), And(y, z))
  E : And(z, Or(x, y)) -> Or(And(z, x), And(z, y))
strategies
  dnf = innermost(E)
```

The first two rules rewrite implication (`Impl`) and equivalence (`Eq`) to combinations of `And`, `Or`, and `Not`.
The third rule removes double negation.
The fifth and sixth rules implement the well known DeMorgan laws.
The last two rules define distribution of conjunction over disjunction.

<!-- We turn this set of rewrite rules into a compilable Stratego program in the same way as before:

```stratego
module prop-dnf
imports prop-dnf-rules
strategies
  dnf = innermost(E)
``` -->

With this definition we can transform `Prop` terms to disjunctive normal form:

```stratego
<dnf> And(Impl(Atom("r"), And(Atom("p"), Atom("q"))), Atom("p"))
   => Or(And(Not(Atom("r")), Atom("p")),
         And(And(Atom("p"), Atom("q")), Atom("p")))
```

<!-- compile it in the usual way

$ strc -i prop-dnf.str -la stratego-lib
so that we can use it to transform terms:

$ cat test3.prop
And(Impl(Atom("r"),And(Atom("p"),Atom("q"))),Atom("p"))
$ ./prop-dnf -i test3.prop
Or(And(Not(Atom("r")),Atom("p")),And(And(Atom("p"),Atom("q")),Atom("p"))) -->
