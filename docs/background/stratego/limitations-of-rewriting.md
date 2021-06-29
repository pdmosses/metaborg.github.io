# Limitations of Rewriting

Term rewriting can be used to implement transformations on programs represented by means of terms.
Term rewriting involves exhaustively applying rules to subterms until no more rules apply.
This requires a strategy for selecting the order in which subterms are rewritten.
The `innermost` strategy applies rules automatically throughout a term from inner to outer terms, starting with the leaves.
The nice thing about term rewriting is that there is no need to define traversals over the syntax tree; the rules express basic transformation steps and the strategy takes care of applying it everywhere.
However, the complete normalization approach of rewriting turns out not to be adequate for program transformation, because rewrite systems for programming languages will often be non-terminating and/or non-confluent.
In general, it is not desirable to apply all rules at the same time or to apply all rules under all circumstances.

Consider for example, the following extension of prop-dnf-rules with distribution rules to achieve conjunctive normal forms:

```stratego
module prop-cnf
imports prop-eval-rules
rules
  E : Or(And(x, y), z) -> And(Or(x, z), Or(y, z))
  E : Or(z, And(x, y)) -> And(Or(z, x), Or(z, y))
strategies
  cnf  = innermost(E)
```

This rewrite system is non-terminating because after applying one of the and-over-or distribution rules, the or-over-and distribution rules introduced here can be applied, and vice versa.

   And(Or(Atom("p"),Atom("q")), Atom("r"))
->
   Or(And(Atom("p"), Atom("r")), And(Atom("q"), Atom("r")))
->
   And(Or(Atom("p"), And(Atom("q"), Atom("r"))),
       Or(Atom("r"), And(Atom("q"), Atom("r"))))
->
   ...
There are a number of solutions to this problem. We’ll first discuss a couple of solutions within pure rewriting, and then show how programmable rewriting strategies can overcome the problems of these solutions.

5.1.1. Attempt 1: Remodularization
The non-termination of prop-cnf is due to the fact that the and-over-or and or-over-and distribution rules interfere with each other. This can be prevented by refactoring the module structure such that the two sets of rules are not present in the same rewrite system. For example, we could split module prop-dnf-rules into prop-simplify and prop-dnf2 as follows:

module prop-simplify
imports prop-eval-rules
rules
  E : Impl(x, y) -> Or(Not(x), y)
  E : Eq(x, y)   -> And(Impl(x, y), Impl(y, x))

  E : Not(Not(x)) -> x

  E : Not(And(x, y)) -> Or(Not(x), Not(y))
  E : Not(Or(x, y))  -> And(Not(x), Not(y))


module prop-dnf2
imports prop-simplify
rules
  E : And(Or(x, y), z) -> Or(And(x, z), And(y, z))
  E : And(z, Or(x, y)) -> Or(And(z, x), And(z, y))
strategies
  main = io-wrap(dnf)
  dnf  = innermost(E)
Now we can reuse the rules from prop-simplify without the and-over-or distribution rules to create a prop-cnf2 for normalizing to conjunctive normal form:

module prop-cnf2
imports prop-simplify
rules
  E : Or(And(x, y), z) -> And(Or(x, z), Or(y, z))
  E : Or(z, And(x, y)) -> And(Or(z, x), Or(z, y))
strategies
  main = io-wrap(cnf)
  cnf  = innermost(E)
Although this solves the non-termination problem, it is not an ideal solution. In the first place it is not possible to apply the two transformations in the same program. In the second place, extrapolating the approach to fine-grained selection of rules might require definition of a single rule per module.

5.1.2. Attempt 2: Functionalization
Another common solution to this kind of problem is to introduce additional constructors that achieve normalization under a restricted set of rules. That is, the original set of rules p1 -> p2 is transformed into rules of the form f(p_1) -> p_2', where f is some new constructor symbol and the right-hand side of the rule also contains such new constructors. In this style of programming, constructors such as f are called functions and are distinguished from constructors. Normal forms over such rewrite systems are assumed to be free of these function symbols; otherwise the function would have an incomplete definition.

To illustrate the approach we adapt the DNF rules by introducing the function symbols Dnf and DnfR. (We ignore the evaluation rules in this example.)

module prop-dnf3
imports libstrategolib prop
signature
  constructors
    Dnf  : Prop -> Prop
    DnfR : Prop -> Prop
rules
  E : Dnf(Atom(x))    -> Atom(x)
  E : Dnf(Not(x))     -> DnfR(Not(Dnf(x)))
  E : Dnf(And(x, y))  -> DnfR(And(Dnf(x), Dnf(y)))
  E : Dnf(Or(x, y))   -> Or(Dnf(x), Dnf(y))
  E : Dnf(Impl(x, y)) -> Dnf(Or(Not(x), y))
  E : Dnf(Eq(x, y))   -> Dnf(And(Impl(x, y), Impl(y, x)))

  E : DnfR(Not(Not(x)))      -> x
  E : DnfR(Not(And(x, y)))   -> Or(Dnf(Not(x)), Dnf(Not(y)))
  E : DnfR(Not(Or(x, y)))    -> Dnf(And(Not(x), Not(y)))
  D : DnfR(Not(x))           -> Not(x)

  E : DnfR(And(Or(x, y), z)) -> Or(Dnf(And(x, z)), Dnf(And(y, z)))
  E : DnfR(And(z, Or(x, y))) -> Or(Dnf(And(z, x)), Dnf(And(z, y)))
  D : DnfR(And(x, y))        -> And(x, y)
strategies
  main = io-wrap(dnf)
  dnf  = innermost(E <+ D)
The Dnf function mimics the innermost normalization strategy by recursively traversing terms. The auxiliary transformation function DnfR is used to encode the distribution and negation rules. The D rules are default rules that are only applied if none of the E rules apply, as specified by the strategy expression E <\+ D.

In order to compute the disjunctive normal form of a term, we have to apply the Dnf function to it, as illustrated in the following application of the prop-dnf3 program:

$ cat test1.dnf
Dnf(And(Impl(Atom("r"),And(Atom("p"),Atom("q"))),Atom("p")))

$ ./prop-dnf3 -i test1.dnf
Or(And(Not(Atom("r")),Atom("p")),
   And(And(Atom("p"),Atom("q")),Atom("p")))
If you’re going to try to run this example in Spoofax/Eclipse, a few words of caution. First, it’s easiest to just accumulate all of the different test modules as imports in your main language “.str” file. But if you do that, all of their rules will be in the same namespace. So you’re going to want to use different identifiers (say “E3” and “D3”) in place of “E” and “D” in your prop-dnf3.str file. Also, the concrete syntax has no way to represent the “extra” function symbol Dnf that is used here, so you’ll want to use alternate triggering strategies like

make-nf  = innermost(E3 <+ D3)
dnf3 : x -> <make-nf> Dnf(x)
that wrap the input in Dnf( ... ) themselves.

For conjunctive normal form we can create a similar definition, which can now co-exist with the definition of DNF. Indeed, we could then simultaneously rewrite one subterm to DNF and the other to CNF.

E : DC(x) -> (Dnf(x), Cnf(x))
In the solution above, the original rules have been completely intertwined with the Dnf transformation. The rules for negation cannot be reused in the definition of normalization to conjunctive normal form. For each new transformation a new traversal function and new transformation functions have to be defined. Many additional rules had to be added to traverse the term to find the places to apply the rules. In the modular solution we had 5 basic rules and 2 additional rules for DNF and 2 rules for CNF, 9 in total. In the functionalized version we needed 13 rules for each transformation, that is 26 rules in total.

In the example repository, you can find both the dnf and cnf strategies in trans/prop-dnf3.str and trans/prop-cnf3.str.
