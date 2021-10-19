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


## Analysis Errors

```stratego
stx-analysis-has-errors = stx--analysis-has-errors
```

Type: `Analysis -> Analysis`

Fails if the current term has _no_ errors, succeeds otherwise.
