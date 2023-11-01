# Stratego API

The Statix solver can be called from a Stratego Transformation using the API in
the [Statix Runtime](https://github.com/metaborg/nabl/tree/master/statix.runtime)
project. After analysis is executed, the analysis result can be queried using
other strategies. In this section, we provide an overview of the availble
strategies.

The public API of the Statix runtime is available
[here](https://github.com/metaborg/nabl/blob/master/statix.runtime/trans/statix/api.str).
This API strongly depends on the Spoofax constraint analysis library, which is
available in the [Spoofax Meta Library](https://github.com/metaborg/spoofax/blob/master/meta.lib.spoofax/trans/libspoofax/analysis/constraint.str).


## Single-File Analysis

```stratego
stx-editor-analyze(pre, post|spec-name, init-constraint)
```

Type: `AnalysisAction -> AnalysisResult`.

Applies single-file analysis with the specification provided in the arguments.
Since this strategy only performs single-file analysis, the current term should
always have `AnalyzeSingle` as top-level constructor. The term and strategy
arguments are explained in the following table:

| Argument          | Type         | Default | Description                                                                                                                                                                                                                                                                                                               |
| :---------------- | :----------- | :------ | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `pre`             | `AST -> AST` | `id`    | Transformation to apply before analyzing. This transformation receives the 'parsed AST'.                                                                                                                                                                                                                                  |
| `post`            | `AST -> AST` | `id`    | Transformation to apply before analyzing. This transformation receives the result of applying `pre` to the 'parsed AST', and yields the 'analyzed AST'.                                                                                                                                                                   |
| `spec-name`       | `String`     |         | The full path to the root module of the specification.                                                                                                                                                                                                                                                                    |
| `init-constraint` | `String`     |         | The name of the constraint that should be applied to the pre-transformed AST. This may be a fully qualified name in the form `$Module!$ConstraintName`, or just a `$ConstraintName`. In the latter case, the name will be qualified with the `spec-name` argument. This constraint should have the (Statix) type `: Start`|

The `post` and `pre` arguments may be omitted (in that order).

Note that this strategy will return _no results_ for `Cached` terms in the analysis action.

## Single-File Elaboration

```stratego
stx-editor-elaborate(pre, post|spec-name, init-constraint)
```

!!! todo
    Find out what this is?


## Multi-File Analysis

```stratego
stx-editor-analyze(pre, post|spec-name, project-constraint, file-constraint)
```

Type: `AnalysisAction -> AnalysisResult`.

Applies multi-file analysis with the specification provided in the arguments.
Since this strategy only performs multi-file analysis, the current term should
always have `AnalyzeMulti` as top-level constructor. This strategy chooses the
solver based on the `metaborg.yaml` configuration of the project and the language.
The term and strategy arguments are explained in the following table:

| Argument             | Type                               | Description                                                                                                                                                                                                                                                                                                                                                             |
| :------------------- | :--------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `pre`                | `AST -> AST`                       | Transformation to apply before analyzing. This transformation receives the 'parsed AST'.                                                                                                                                                                                                                                                                                |
| `post`               | `AST -> AST`                       | Transformation to apply before analyzing. This transformation receives the result of applying `pre` to the 'parsed AST', and yields the 'analyzed AST'.                                                                                                                                                                                                                 |
| `spec-name`          | `String`                           | The full path to the root module of the specification.                                                                                                                                                                                                                                                                                                                  |
| `project-constraint` | `String`                           | The name of the constraint that should be applied to the global scope once. This may be a fully qualified name in the form `$Module!$ConstraintName`, or just a `$ConstraintName`. In the latter case, the name will be qualified with the `spec-name` argument. This constraint should have the (Statix) type `#!statix : scope`                                       |
| `file-constraint`    | `String`                           | The name of the constraint that should be applied to the pre-transformed AST of each file in the project. This may be a fully qualified name in the form `$Module!$ConstraintName`, or just a `$ConstraintName`. In the latter case, the name will be qualified with the `spec-name` argument. This constraint should have the (Statix) type `#!statix : scope * Start` |


## Concurrent Analysis

```stratego
stx-editor-analyze(pre, group, post|spec-name, project-constraint, group-constraint, file-constraint)
```

Type: `AnalysisAction -> AnalysisResult`.

Applies concurrent multi-file analysis with the specification provided in the
arguments. Since this strategy only performs multi-file analysis, the current
term should always have `AnalyzeMulti` as top-level constructor. This strategy
chooses the solver based on the `metaborg.yaml` configuration of the project and
the language, but fails with a fatal error if the concurrent solver is not
enabled on this project. The term and strategy arguments are explained in the
following table:

| Argument             | Type                               | Description                                                                                                                                                                                                                                                                                                                                                             |
| :------------------- | :--------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `pre`                | `AST -> AST`                       | Transformation to apply before analyzing. This transformation receives the 'parsed AST'.                                                                                                                                                                                                                                                                                |
| `group`              | `(Resource * AST) -> List(String)` | Strategy that decides in which group a resource is analyzed. Should return a list with the identifiers of the groups in which the resource should be analyzed.                                                                                                                                                                                                          |
| `post`               | `AST -> AST`                       | Transformation to apply before analyzing. This transformation receives the result of applying `pre` to the 'parsed AST', and yields the 'analyzed AST'.                                                                                                                                                                                                                 |
| `spec-name`          | `String`                           | The full path to the root module of the specification.                                                                                                                                                                                                                                                                                                                  |
| `project-constraint` | `String`                           | The name of the constraint that should be applied to the global scope once. This may be a fully qualified name in the form `$Module!$ConstraintName`, or just a `$ConstraintName`. In the latter case, the name will be qualified with the `spec-name` argument. This constraint should have the (Statix) type `#!statix : scope`                                       |
| `group-constraint`   | `String`                           | The name of the constraint that should be applied to the each group. This may be a fully qualified name in the form `$Module!$ConstraintName`, or just a `$ConstraintName`. In the latter case, the name will be qualified with the `spec-name` argument. This constraint should have the (Statix) type `#!statix : scope * string * scope`                             |
| `file-constraint`    | `String`                           | The name of the constraint that should be applied to the pre-transformed AST of each file in the project. This may be a fully qualified name in the form `$Module!$ConstraintName`, or just a `$ConstraintName`. In the latter case, the name will be qualified with the `spec-name` argument. This constraint should have the (Statix) type `#!statix : scope * Start` |


## Constraint Evaluation

```stratego
stx-evaluate(|spec-name, constraint)
```

Type: `List(Term) -> Term`

Evaluates a _functional constraint_. The terms in the current term are passed
as argument to the constraint, and the result term is the output term of the
constraint.

| Argument          | Type         | Description                                                              |
| :---------------- | :----------- | :----------------------------------------------------------------------- |
| `spec-name`       | `String`     | The full path to the root module of the specification.                   |
| `constraint`      | `String`     | The name of the constraint that should be applied to the term arguments. |


## Reading Analysis Results

The Statix API provides several strategies to query properties from the analysis.
These strategies are dicussed in the following sections.

First of all, the analysis result can be obtained by the following strategy:

```stratego
stx-get-ast-analysis
```

Type: `Term -> Analysis`

The `stx-get-ast-analysis` returns the Analysis object for an AST. This object
can later be used to query the scope graph and AST properties set by the
Statix specification.

Note that the passed AST should be an analyzed AST. For Spoofax 2 use cases,
this means that this strategy can only be used in builders without the
`#!esv (source)` annotation.

The returned values will be interpreted relative to the unifier of the analysis.
That is, it will be instantiated as much as possible. When a property value
contains free variables, those will occur in the property as
`nabl2.Var: String * String -> Term` terms.

## Properties

AST properties can be extracted from the analysis result using the following strategy:

```stratego
stx-get-ast-property(|a, name)
```

Type: `Term -> Term or list(Term)`.

| Argument  | Type         | Description                               |
| :-------- | :----------- | :-----------------------------------------|
| `a`       | `Analysis`   | Analysis object for the given AST node.   |
| `name`    | `String`     | The name of the property that is queried. |

Given an AST node, this strategy will return the property value. For singleton
properties (`#!statix :=` operator), the property value is returned. For bag
properties (`#!statix +=` operator), a list with all assigned values is returned.
It fails if no property with the given name is set. Therefore, for bag properties
the resulting list will never be empty.

*Example 1.* Consider a Statix specification that contains a `#!statix @t.prop := val`
constraint. Using `#!statix <stx-get-ast-property(|a, "prop")> t` will then
return `val`

*Example 2.* Consider a Statix specification that contains
`#!statix @t.prop += val1, @t.prop += val2` constraints. Using
`#!statix <stx-get-ast-property(|a, "prop")> t` will then
return `[val1, val2]`.

As the `type` and `ref` properties have special meanings in the Spoofax context,
there are special strategies to retrieve those:
```stratego
stx-get-ast-type(|a)

stx-get-ast-ref(|a)
```
which both have the same type constraints as `#!stratego stx-get-ast-property`

!!! warning "`type` and `ref` properties"
    Using the generic `#!stratego stx-get-ast-property` to retrieve `type` or
    `ref` properties will not work. I.e., `#!stratego stx-get-ast-property(|a, "type")> t`
    will fail, even if there was an `#!statix @t.type := T` constraint.


## Scope Graph

Declarations in a scope graph can be retrieved using the following strategies:

```stratego
stx-get-scopegraph-data(|a, rel)

stx-get-scopegraph-edges(|a, lbl)
```

| Argument  | Type         | Description                                           |
| :-------- | :----------- | :-----------------------------------------------------|
| `a`       | `Analysis`   | Analysis object for the given AST node.               |
| `rel`     | `String`     | Fully qualified name of the relation that is queried. |
| `lbl`     | `String`     | Fully qualified name of the label that is traversed.  |

The `#!stratego stx-get-scopegraph-data` strategy, which has type `Scope -> [Term]`
retrieves all data declared under relation `rel` in the input term scope. The
data is returned in a (possible empty) list that contains tuples holding the
data of each relevant declaration.

*Example.* Consider a Statix specification that gives rise to a
`#!statix new s, !var["x", INT()] in s, !var["y", BOOL()] in s` constraint. Now,
applying `#!stratego <stx-get-scopegraph-data(|a, "statics/Main!var")> s` will
return `[("x", INT()), ("y", BOOL())]`.

Note that a fully qualified name should be passed to the `rel` argument. Fully
qualified names are created by prefixing a relation name with the module in
which it is declared, separated by a `!`. For example, `#!stratego "statics/Main!var"` is
the fully qualified name of the relation `var` declared in module `#!statix statix/Main`.
The Spoofax 2 Console will emit warnings when an invalid label is used, and
suggest available names.

The returned values will be interpreted relative to the unifier of the analysis.
That is, it will be instantiated as much as possible. When a property value
contains free variables, those will occur in the property as
`nabl2.Var: String * String -> Term` terms.

The `#!stratego stx-get-scopegraph-edges` strategy, which has type `Scope -> [Scope]`
traverses all edges with the `lbl` label. All target scopes are returned in the
output list.

*Example.* Consider a Statix specification that gives rise to a
`#!statix new s s1 s2, s -L-> s1, s -L-> s2` constraint. Now, applying
`#!stratego <stx-get-scopegraph-edges(|a, "statics/Main!L")> s` will return
`[s1, s2]`.

Similar to the `#!stratego stx-get-scopegraph-edges` strategy, the label should
be fully qualified, and the result may contain free variables.

??? tip "Retrieving a scope"
    Both strategies discussed in this section take a scope as input. However, it
    seemed that no way to obtain a reference to a scope was introduced. In fact,
    scope references should be made available using AST properties. For example,
    the `#!statix new s, @t.scope := x` makes scope `s` available using the
    `#!stratego stx-get-ast-property(|a, "scope") t` transformation.


## Analysis Results

```stratego
stx-analysis-has-errors = stx--analysis-has-errors
```

Type: `Analysis -> Analysis`

Fails if the current term has _no_ errors, succeeds otherwise.
