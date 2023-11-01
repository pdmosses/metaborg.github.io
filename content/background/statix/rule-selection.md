# The Semantics of Rule Selection

In this background article, we consider the precise semantics of
Statix' rule selection, and motivate it. In [the first section](#the-anatomy-of-a-user-defined-constraint)
we consider the components of which a user-defined constraint in Statix is composed. After
that, we [consider how a constraint is solved](#solving-a-user-defined-constraint).
Next, we [explain how Statix chooses an appropriate rule for a constraint](#choosing-from-multiple-applicable-rules),
and finally, we [explain the analysis](#guaranteeing-rule-selection-uniqueness)
Statix performs over specifications that guarantees that, for any
constraint with ground arguments, at most one single rule is available.


## The Anatomy of a User-Defined Constraint

Statix allows users to define their own constraints. Before explaining how these
constraints are evaluated, we explain the components of which user-defined
constraints and their rules are built. We use the following specification
snippet as an example.

```statix
rules

  typeOfExpr: scope * Expr -> TYPE

  [T-Int]typeOfExpr(s, IntLit(_)) = INT().

  [T-Add]typeOfExpr(s, Add(e1, e2)) = INT() :-
    typeOfExpr(s, e1) == INT(),
    typeOfExpr(s, e2) == INT().
```

In this example, a user-defined constraint `typeOfExpr` is defined. A user
constraint consists of a _constraint declaration_ and a collection of rules.
A constraint declaration (line 3 of the example) introduces a user constraint by
declaring its name and signature. This declaration indicates that propositions
of the form `#!statix typeOfExpr/3` can be proven. In order to prove such
statements, rules (such as `T-Int` and `T-Add`) can be declared.

Rules can be split in two parts: the _head_ and the _body_. The head is the part
before the turnstile (`:-` symbol), while the body comes after it. Declaratively,
such rules read as "from _body_, _head_ can be derived".

A rule head consists of three components: the rule name, the constraint id, and
the head pattern. The rule name (`T-Int` and `T-Add` in the example) is optional,
and only serves documentation purposes. The constraint identifier indicates the
predicate for which this rule can prove constraints. Finally, the head pattern
determines which constraints can be proven using this rule.


## Solving a User-Defined Constraint

Given such constraint simplification rules, how can we solve constraints with
them? The way this works in Statix is as follows. Statix takes a _top-down_
approach. This means that it starts with an initial constraint, which it will
simplify until a solution for the original constraint is found. For a
user-defined constraint, this simplification proceeds in three steps:

1. Based on the predicate arguments, a matching rule is selected. A rule matches
   a constraint when the constraint arguments match agains the head pattern.
2. Based on the match, all head pattern variables in the constraint body are
   substituted with the values assigned to them by the head matching.
3. All constraints in the substituted body are added to the active constraint
   set, while the original (now simplified) constraint is removed from
   the set of active constraints.

For example, suppose the initial constraint is `#!statix typeOfExpr(#s, Add(IntLit(20), IntLit(22))) == INT()`.
This constraint only matches the `T-Add` rule. Therefore that rule is selected.
When matching the following pattern variable bindings are created:
```statix
  s  |-> #s
  e1 |-> IntLit(20)
  e2 |-> IntLit(22)
```
These bindings are substituted in the body of the `T-Add` rule, yielding the
following constraints:

```statix
  typeOfExpr(#s, IntLit(20)) == INT()
  typeOfExpr(#s, IntLit(22)) == INT()
```
These constraints are added to the set of active constraints, and then
subsequently solved.


## Choosing from Multiple Applicable Rules

Now the question naturally arises what happens when multiple rules can be applied
to try to solve a single constraint. For example, consider solving the constraint
`#!statix subtype(NULL(INT()), NULL(INT()))` using the following specification.
```statix
rules

  subtype: TYPE * TYPE -> TYPE

  [S-Eq]subtype(T, T).

  [S-Null]subtype(NULL(T1), T2) :-
    subtype(T1, T2).
```
Both rules can be used to simplify the original constraint, but only `S-Eq` will
ensure the constraint will be solved. Selecting `S-Null` yields
`#!statix subtype(NULL(INT()), INT())`, as simplified constraint, for which no
applicable rule exists.

At a first glance, the most robust option seems to try all possible rules, until
a rule is found that ensures the constraint is solved. When the simplified
constraints of a particular rule application cannot be fully solved, the
modifications to the solver state are undone, and another rule is tried.

However, there are multiple problems with this approach. Perhaps most important,
in a type-system we prefer to assign _principal types_. Principal types should
be unique, and correspond to a _minimal model_. However, for such a backtracking
approach, it is not guaranteed that a unique minimal solution for a constraint
exists. For example, consider solving `#!statix lub(INT(), INT()) == ?T` with
the following specification:

```statix
rules
  lub: TYPE * TYPE -> TYPE

  lub(T, T) = T.
  lub(_, _) = ANY().
```
In this case, the rules show that both `?T |-> INT()` and `?T |-> ANY()` are
solutions for this problem. However, one cannot derive from the specification
(with the backtracking semantics) which solution is the intended one.

Additionally, backtracking comes with significant performance drawbacks.
Consider backtracking on an edge assertion. All scope graph queries that
traversed that edge now need to be undone, including all constraints over their
answers. Although it is never tried for Statix itself, we expect such operations
to become very bad in performance, limiting the scalability of Statix.

_Specificity Ordering._
Instead of backtracking, we employ a _committed choice_ approach. That is, once
Statix selects a rule, it will never backtrack on that choice. The rule that is
selected is not arbitrary, but instead Statix tries to find the _most specific_
rule that applies to the constraint. More precisely, the 'most specific'
rule to select is determined as follows. First, we call the collection of term
that match on a pattern the _domain_ of the pattern. For example, `NULL(T)`
matches `NULL(INT())` and `NULL(BOOL())` (i.e., those are in the domain of
`NULL(T)`), but not `INT()`. Second, we call a pattern P1 _more specific_ than
another pattern P2 when the domain of P1 is strictly contained in the domain of
P2. So, for example, the pattern `NULL(INT())` is more specific than `NULL(_)`,
but of `FUN(BOOL(), _)` and `FUN(INT(), _)`, neither is more specific than the
other. We use this notion of pattern specificity to deterministically select a
rule for a constraint as follows. When two rules (say R1 and R2) can both be
used to solve a constraint C, we compare the argument patterns from R1 and R2
from left to right, and select the rule for which we first encounter a more
specific pattern. This way of ordering rules is usually referred to as
_specificity ordering_.

We explain this rule by applying them to the previous examples. Consider the
rules `S-Eq` and `S-Null` again. When comparing these rules, first the patterns
`T` (from `S-Eq`) and `NULL(T)` (from `S-Null`) are compared. It can easily be
seen that `T` is more generic that `NULL(T)`. Therefore, for the example
constraint, `S-Null` is chosen.

An attentive reader might observe that choosing `S-Null` is perhaps not the
intended choice of the specification writer. To solve this, an additional rule
`#!statix subtype(NULL(T), NULL(T))` (or, shorter but equivalent:
`#!statix subtype(T@NULL(_), T)`) must be added. This rule takes precedence
over the first rule, because `NULL(T)` is more specific than `T`. Moreover, it
is also preferred over the second rule, as the following discussion will explain.

_Non-linear Patterns._
Looking to the `#!statix lub(INT(), INT())` example, we first compare `T` with `_`.
As both of them match all terms of their sort, they are considered equal. Hence the rule
selection procedure continues with comparing the second pair of arguments.
Again, the patterns `T` and `_` are compared. While it seems that these patterns
are again similar, that is not actually the case. Because the `T` variable did
already occur earlier (that is, more to the left) in the pattern, its domain is
restricted to the value assigned to the first occurrence of `T`. Therefore, the
first constraint is selected, and `INT()` is determined to be the unique upper
bound of two `INT()` types.

To see why this treatment of non-linear patterns (i.e., patterns in which a
variable occurs multiple times) makes sense, consider selecting a rule for
`#!statix lub(INT(), BOOL()) == ?T`. It is obvious that this constraint does
not match the first rule, because the pattern variable `T` cannot be assigned
both `INT()` and `BOOL()` at the same time. In the selection strategy outlined
in the previous paragraph, this is accounted for by treating the second `T` as
restricted to the value of its first occurrence.

This leads us to a last subtlety. Consider the constraint `c(C(), C(), C())` in
the following specification:
```statix
rules
  c: S * S * S

  [C-1]c(T, _, T).
  [C-2]c(_, T, T) :- false
```
Applying the left-to-right comparison will regard the first two argument pairs
equal, as both compare a wildcard with a new variable. When comparing the third
pair of patterns (`T` and `T`), both of them are restricted by their earlier
occurrence. In order to 'break ties' here, the rule in which the bound variable
occurred _the earliest_ is chosen. In this case, the `T` occurred at argument
position 1 in `C-1`, while it occurred at position 2 in `C-2`. Therefore, for
this constraint, rule `C-1` is chosen.

In summary, given two applicable rules for a constraint, the rule to choose is
decided using the following rules:

1. When pairwise comparing the arguments of the rules from left to right, the
   rule for which a more specific argument pattern is encountered first is
   chosen.
2. For non-linear patterns, a second occurrence of a variable is regarded as
   more specific than a first occurrence of a variable. When both variables are
   bound already, the one bound the earliest is considered the most specific.


## Guaranteeing Rule Selection Uniqueness

The rules outlined above cannot prioritize all pairs of rules. Therefore Statix
statically prevents rules with overlapping patterns. In this section, we discuss
which rule patterns are not allowed to co-exist.

Obviously, two _equivalent_ patterns is not allowed. Consider for example the
following specification:
```statix
rules
  rule: S * S

  rule(T, T).
  rule(S, S) :- false.
```
In this specification, there are two rules with fully equivalent patterns. Thus
it is not possible to prioritize a particular rule over another. Therefore Statix
will statically reject this specification.

More intricate cases happen when non-linear patterns are involved. Consider this
specification as an example:
```statix
rules
  subtype: TYPE * TYPE

  [S-Null]subtype(_, NULL()).
  [S-Any]subtype(_, ANY()).

  [S-Eq]subtype(T, T).
```
In this specification, `S-Null` and `S-Any` can co-exist without problems,
because their domains do not overlap. However, this does not hold for `S-Null`
and `S-Eq`, because `subtype(NULL(), NULL())` matches both. In addition, they
cannot be ordered using the rule ordering we explained so far. The first terms
(`_`) are obviously equal, while the second terms (`#!statix NULL()` and
`#!statix ANY()`) have no ordering. To prevent such runtime non-determinism,
Statix will statically compare all rule heads using the rules outlined above.
In case the heads of a pair of rules have overlapping domains, but can not be
ordered (such as `S-Eq` and `S-Null`), a static error is emitted.

On the subset of possible rules that adheres to the static analysis described
above, an ordering is defined on _any pair of rules with overlapping domains_.
Therefore, for each constraint, a single rule is selected deterministically.
This ensures constraints have a unique solution, giving Statix the desirable
properties of confluence and efficiency.


## Conclusion

Statix uses a deterministic, committed-choice, rule selection mechanism
to solve user-defined constraints. The choice mechanism prefers rules
with a smaller domain (if applicable) over more general ones. In case
of incomparable domains, a left-to-right comparison of the individual
arguments is made. A static analysis on Statix specifications ensures
there exist no rules that incomparable using this method in a real
specification.
