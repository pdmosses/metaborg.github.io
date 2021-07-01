# Queries

Scope Graphs, as introduced in the [previous section](../scope-graphs) can be
queried. Scope graph queries always start in a particular scope, and traverse
the scope graph in order to find declarations under a particular relation. The
syntax for queries is as follows:

```statix
query $QueryTarget
   filter $LabelRE and $DataWF
      min $LabelOrder* and $DataLeq
       in $Scope |-> $Result
```

The `$Scope` parameter is a term with type `scope`. In this scope, the query starts.
All other query arguments are explained in the following subsections.

## Query Targets

The query target is the 'thing' that is looked for in the query. This can be one of:

- `$Relation`: A _relation identifier_. In this case, the query will return data
  that is declared under that relation.
- `()`: the _end of path_ query target. In this case, the query will return all
  paths that match the appropriate filters.

??? hint "`()` as relation"
    The `()` query target can be thought of as a regular relation if one assumes
    `#1 |-()-> #1` to exist for every scope `#1` in the scope graph.


## Filters

Query results can be filtered using two different filters. First, a regular
expression on labels (`$LabelRE`) defines a filter on the paths that the query
resolution algorithm will explore. This regular expression can be build from
the following components:

- `$Label`: Matches paths that travers a single edge with the label `$Label`.
  Requires the label to be declared in a `signature` section, as explained in
  the section on [edges](../scope-graphs#edges).
- `e`: _epsilon_. Matches the empty path. Queries using this filter will only return
  declarations in the scope where the query started.
- `0`: _empty set_. Matches no path.
- `$LabelRE $LabelRE`: _concatenation_. Matches paths that can be split in two
  segments `p1` and `p2`, such that `p1` matches the first regular expression,
  and `p2` matches the second.
- `$LabelRE | $LabelRE`: _disjunction_. Matches paths that match either the first
  or the second regular expression.
- `$LabelRE & $LabelRE`: _conjunction_. Matches paths that match both the first
  and the second regular expression.
- `~$LabelRE`: _negation_. Matches all paths that do _not_ match the inner
  regular expression.
- `$LabelRE*`: _closure_. Matches paths that can be split into zero or more
  segments that each match the inner regular expression.
- `$LabelRE+`: _one or more_. Matches paths that can be split into one or more
  segments that each match the inner regular expression. Equivalent to
  `$LabelRE $LabelRE*`
- `$LabelRE?`: _zero or one_. Matches paths that are matched by the inner regular
  expression, or empty paths. Equivalent to `$LabelRE | e`.

Additionally, regular expression can be grouped by brackets.

Second, _data well-formedness_ filters (`$DataWF`) can be applied. These filters
restrict which datums are included in the query result. They are expressed as
anonymous lambda rules:

```statix
{ $Pattern :- $Constraint }
```

This rule is instantiated for every [declaration](../scope-graphs#declarations)
that is reachable according to the path well-formedness expression. When the
instantiated body constraint holds, the declaration is included in the query
answer.

??? info "Lambda Instantiation"
    Lambda constraint instantiation is similar to rule instantiation. For more
    information on rule instantiation, see the section about
    [rule definitions](../rules#rule-definitions).

??? info "Entailment semantics"
    Data well-formedness conditions are treated as entailment/implied conditions.
    Hence, they are not allowed to extend or refine the outer context. For more
    information on this evaluation mode, see the documentation of the
    [`try` construct](../basic-constraints#try).

The type of the predicate that is expected depends on the kind of relation that
is used. For predicative relations, all arguments in the relation are provided
to the data well-formedness constraint. However, for functional relations, the
'output value' (i.e. the value that the relation maps to) is _not_ provided to
the filter.

When multiple arguments are provided to a data-wellformedness predicate
(when there are multiple 'input' arguments to the queried relation), these
arguments must be wrapped in a tuple.

When the end-of-path query target `()` is used, the data-wellformedness constraint
expects a single scope as argument.

??? example "Example of filters"
    A simple query for variables illustrates both filters. Suppose the relation
    `var` is in scope with type `string -> TYPE`. Then a rule (with
    [type ascriptions](../terms#type-ascription)) that looks up a
    variable definition can be defined as follows.
    ```statix
    resolveVar(s : scope, name : string) = R :-
      query var
        filter P* I?
           and { name' : string :- name' == name }
        in s |-> R.
    ```
    In this example, the path well-formedness expression `P* I?` indicates that
    any number of `P` edges may be traversed, and then, optionally, a single `I`
    edge. This resolution policy excludes e.g. transitive imports, and the
    traversal of `P` edges in an imported module.

    The anonymous data well-formedness condition states that a declaration
    with name `name'` may only be included in the query result if `name'` is
    equal to `name` from the enclosing scope. Suppose that `resolveVar` is
    instantiated for `name |-> "x"`, and declarations with name `"x"` and `"y"`
    are in scope. Now the anonymous inner rule is instantiated for both `"x"`
    and `"y"`. For `"x"`, the constraint `"x" == "x"` is generated, which can be
    solved successfully. For `"y"` however, the constraint `"y" == "x"` is
    generated, which cannot be solved successfully. Hence, only the declaration
    for `"x"` is included in the eventual query answer.

There are two shorthands for common data well-formedness predicates:

- `true`, which is equivalent to `{ _ :- true }`. This shorthand
  will thus include all encountered declaration in the query result.
- `false`, which is equivalent to `{ _ :- false }`. This shorthand
  will include no declarations in the query answer.
<!---
This pattern does not yet work correctly
- `{ $Pattern }`, is equivalent to `{ $Pattern :- true }` and hence will include
  all declarations that match `$Pattern`.
-->
Syntactically, the query filter can be omitted entirely, or the data well-formedness
predicate can be omitted, even if a path filter is provided. By default, the
path filter is `~0`, meaning that every path is considered valid, and the data
well-formedness predicate is `true`, meaning that every datum will be returned
in the query answer.


## Shadowing

For many languages, name resolution involves dealing with shadowing correctly.
In Statix queries, it is possible to encode shadowing policies using label orders
and data comparison predicates. A declaration shadows another declaration iff
its path is 'smaller than' the other path by a prefix order defined over a label
comparison relation, and when the declaration data is smaller than or equal to
the data of the other declaration according to a data comparison predicate.

Label orders (`$LabelOrder`) are expressed as less-than relations on labels.

```statix
$Label < $Label
```

Here, a label is either a [declared label symbol](../scope-graphs#edges), or `$`,
which denotes the 'end-of-path' label. This label can be used to express orders
on path length. For example, `$ < P` expresses that paths with fewer `P` labels
are preferred over paths with more `P` labels.

!!! warning "Strict Partial Order"
    Label orders must be _strict partial orders_. That is, they are implicitly
    transitive, but may not be reflexive or symmetric. Label order specifications
    that are not strict partial orders will be rejected at specification loading
    time.

??? warning "Prefix order"
    Note that the label order is a _prefix order_, not a _lexicographical
    full-path order_. That is, paths that diverged by traversing different edges
    with the same label are not ordered by this relation.

In addition to a label ordering relation, a data comparison predicate (`$DataLeq`)
can be provided. This predicate can be written as follows:

```statix
{ $Pattern, $Pattern :- $Constraint }
```

This constraint indicates that the left argument is smaller than the right
argument, given that the constraint can be satisfied.

The types of each patterns is similar to the type of the data-wellformedness
predicate. When the queried relation is predicative (i.e. has no 'output'),
the pattern is a tuple containing arguments of the declaration that is compared.
If the queried relation is functional, a tuple with only the 'input' arguments
must be provided. When there is only one declaration argument, the tuple may be
omitted.

There are several shorthands available for the data comparison constraint:

- `true` is equivalent to `{ _, _ :- true }`, and hence ensures that declarations
  are shadowed based on the label order only.
- `false` is equivalent to `{ _, _ :- false }`, and hence ensures that no
  shadowing is applied, even when paths can be ordered using the label order.
- `$ConstraintName` is equivalent to `{ d1, d2 :- $ConstraintName(d1, d2) }`,
  which means that `d1` shadows `d2` when `$ConstraintName(d1, d2)` can be
  satisfied.
- `{ $Pattern, $Pattern }` is equivalent to `{ $Pattern, $Pattern :- true }`,
  which means that the first argument shadows the second if they match the
  patterns.

??? tip "Non-linear Patterns"
    The data comparison shorthand is mostly used with non-linear patterns. For
    example, to encode that declarations with equal names shadow each other,
    the data comparison shorthand `{ x, x }` can be used. When using this pattern
    however, please ensure that variable names are fresh, because the behavior
    of shadowing names is planned to change in the future.

??? warning "Partial Order"
    Data comparison functions orders must be _(non-strict) partial orders_. That
    is, they are implicitly transitive and reflexive, but may not be symmetric.
    However, this is not validated for tractability reasons. Therefore, for any
    predicate that is not a partial order (other than `true`), shadowing
    behavior is undefined.

Syntactically, the shadowing parameters can be omitted altogether, or the data
comparison predicate can be omitted, even when an label order is specified. The
default value of the label order is an empty relation, while the default value
of the data comparison predicate is `true`. On the one hand, this ensures that
no shadowing is applied when no shadowing parameters are provided. On the other
hand, when a label order, but no data comparison predicate is provided, all
declarations shadow each other based on a path comparison only.

Operationally, the label order and the data comparison constraints are applied
_conjunctively_. For any declaration `d` and `d'`, if the path to `d` is smaller
than the path to `d'` according to the label order, _and_ the application of the
data comparison constraint to `d, d'` can be satisfied, `d'` will be excluded
from the query answer.


## Result Pattern

When the query resolution is completed, the query result will be unified with
the `$Result` term. This term is a list that contains path-datum entries.
Therefore, the type of this term is `list((path * R))`, where `R` is a tuple
type with the argument types of the relation that is queried. In case the
relation is functional, the 'output' type is _included_ in the result. When the
relation is unary, the tuple is omitted. When the [query target](#query-target)
is `()`, `R` is the `scope` type.

For the syntactic structure of the paths, please refer to the section on
[path terms](../terms#paths). Semantically, for any query answer pair `(p, d)`,
the path `p` represents the path followed from the scope in which the query
started to the scope in which the declaration of `d` was found.

??? info "Top-level Destination scope"
    Since path terms are _left-recursive_, have the source scope at the left
    side, and the destination scope (i.e. the scope in which the paired
    datum was declared) on the right, it turns out that the target scope is in
    the third argument of the _top-level_ constructor. This is convenient, since
    it allows to access the target scope without destructuring the whole path.
    (Direct access to the source scope is not really important, since it is
    already available as an argument to the query constraint). On the other
    side, it is sometimes perceived as not completely intuitive to have the
    target scope in the top level constructor.

When multiple results are returned by the query, Statix has no guarantees on the
order of their appearence in the list.


## Query Sugar

!!! warning
    Since Spoofax 2.5.15, the query sugar constructs are deprecated.
