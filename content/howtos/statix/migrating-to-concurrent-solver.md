# Migrating to the Concurrent Solver

In this how-to guide, we explain what changes should be made to enable the
concurrent solver for a Statix project.


## Enabling the Concurrent solver for a Language

To enable the concurrent solver for a language, set the `language.statix.concurrent`
property in the `metaborg.yaml` file to `true`. This ensures that the
concurrent solver is used for all sources in the language.

```yaml
id: org.example:mylang:0.1.0-SNAPSHOT
name: mylang
language:
  statix:
    mode: concurrent
```


## Enabling the Concurrent solver for an Example Project only

To enable the concurrent solver for a particular project only, set the
`runtime.statix.modes` property in the `metaborg.yaml` file to a map
that contains all names of the languages for which you want to use the
concurrent solver, and their corresponding modes. The name of the language
should correspond to the `name` property in the `metaborg.yaml` of the
language definition project.


```yaml
id: org.example:mylang.example:0.1.0-SNAPSHOT
runtime:
  statix:
    modes:
    - mylang: concurrent
```

## Indirect Type Declaration

Type checking with the concurrent solver might result in
deadlock when type-checkers have mutual dependencies on their declarations.
This problem can be solved by adding an intermediate declaration that splits
the part of the declaration data that is filtered on (usually the declaration
*name*), and the part that is processed further by the querying unit (usually
the *type*). This pattern is best explained with an example:

```statix
signature
  relations
    type : ID -> TYPE

rules
  declareType : scope * ID * TYPE
  resolveType : scope * ID -> TYPE

  declareType(s, x, T) :-
    !type[x, T] in s.

  resolveType(s, x) = T :-
    query type
      filter P* I* and { x' :- x' == x }
          in s |-> [(_, (_, T))].
```

This specification needs to be changed in the following:

```statix
signature
  relations
    type   : ID -> scope
    typeOf : TYPE

rules
  declareType : scope * ID * TYPE
  resolveType : scope * ID -> TYPE

  declareType(s, x, T) :-
    !type[x, withType(T)] in s.

  resolveType(s, x) = typeOf(T) :-
    query type
      filter P* I* and { x' :- x' == x }
          in s |-> [(_, (_, T))].
          
rules
  withType : TYPE -> scope
  typeOf   : scope -> TYPE

  withType(T) = s :-
    new s, !typeOf[T] in s.

  typeOf(s) = T :-
    query typeOf filter e in s |-> [(_, T)].
```

We now discuss the changes one-by-one. First, the signature of relation `type`
is be changed to `ID -> scope`. In this scope, we store the type using the
newly introduced `typeOf` relation. This relation only carries a single `TYPE`
term. In this way, the original term is still indirectly present in the outer
declaration.

The `withType` and `typeOf` rules allow to convert between these representations.
The `withType` rule creates a scope with a `typeOf` declaration that contains
the type.  In the adapted `declareType` rule, this constraint is used to
convert the `T` argument to the representation that the `type` relation accepts.
Likewise, the `typeOf` rule queries the `typeOf` declaration to extract the
type from a scope. This rule is used in the `resolveType` rule to convert
back to the term representation of a type.

Performing this change should resolve potential deadlocks when executing your
specifications. Because the signatures of the rules in the original specification
did not change, and the new specification should have identical semantics,
the remainder of the specification should not be affected.

## Using Grouping

The traditional solver uses two special constraints as entry points: the
*project constraint* (usually named `projectOk`) was solved once for each
project, while the *file constraint* (usually called `fileOk`) was solved for
each file in that project. The concurrent solver adds the concepts of *groups*
in between these concepts. Files can be organized in groups, while groups can
in addition contain subgroups. This gives rise to a tree-shaped hierarchy, where
the project is the root node, the files are the leaf nodes, and all nodes in
between are groups. Most often, this hierarchy follows the directory structure
of a project. In order to use grouping, two steps need to be performed.

First, a *group constraint* must be defined. The group constraint must have the
signature `#!statix scope * string * scope`. For each group, this constraint
will be instantiated with the parent group scope, group name and own group scope
as arguments (in that order).

A simple example of a group constraint can look as follows:

```statix
signature

  sorts MODULE constructors
    MODULE: scope -> MODULE

  relations
    mod: string * MODULE

rules

  groupOk: scope * string * scope
  groupOk(s_prnt, name, s_grp) :-
    !mod[name, MODULE(s_grp)] in s_prnt.

```

In this fragment, we define the `groupOk` constraint, which has the appropriate
signature. The body of the rule for this constraint simply declares that a module
with the appropriate name exists in the parent scope.

Second, the builder needs to be adapted in two ways: the name of the group
constraint must be passed to the solver, and a strategy that determines the group
of a file must be provided to the solver. Such a strategy should have type
`#!stratego (String * AST) -> List(String)`. The input arguments represent the
file path and its AST, respectively. The output list should contain all group
identifiers from project root to the respective file. For example, a Java
specification should return `["java", "lang", "Object"]` for the `Object` class
in the `java.lang` package. Note that the file must be assigned a name, and that
that name should be included in the output list.

A project that uses the directory structure as its grouping structure could
call the `stx-editor-analyze` as follows:

```stratego
rules

  editor-analyze = stx-editor-analyze(pre-analyze,group-key,post-analyze|"statics", "projectOk", "groupOk", "fileOk")

  group-key: (resource, ast) -> key
    with rel-path := <current-language-relative-source-or-include-path> resource
       ; key := <string-tokenize> (['/','\'], rel-path)
```

In this snippet, the `#!stratego "groupOk"` argument between the file and project
constraint names points to our newly defined group constraint. The `#!stratego group-key`
strategy, passed between the pre and post transformation strategies, is the
strategy that performs the grouping. It first makes the path relative to the
project root, and then splits it on each `'/'` or `'\'` character.

## Using Libraries

Secondly, the concurrent solver allows to export the scope graph of a project in
a library. These libraries can be linked with other projects, potentially
decreasing analysis times significantly. Statix libraries can be generated and
linked by following three steps.

As a first step, use the `#!gui Spoofax ‣ Statix ‣ Make project library` menu on
a file in your library project to export its scope graph. A `project.stxlib`
file will now appear in the root directory of that project.

!!! warning "Project Scope Configuration"
    Currently, the project scope in the `project.stxlib` file must still be configured
    manually. Some understanding of the Statix library format is helpful for that.
    The signature for Statix libraries looks roughly as follows:

    ```statix
    sorts Library constructors
      Library : list(Scope) * list(Scope) * ScopeGraph -> Library

    sorts ScopeGraph constructors
      ScopeGraph: list((Scope * Datum? * list(Edge))) -> ScopeGraph
    ```

    The top-level `Library` term contains (in this order): the list of shared scopes,
    the list of all scopes of the library, and the actual scope graph.
    A scope graph consists of scope entries, which are defined as three-tuples of:
    scope, datum associated to that scope, and the list of outgoing edges for that scope.

    In order to configure the root scopes correctly, perform the following steps:

    1. Identify the project scope. Names of the project scope are:
       `Scope("/.", "s_prj-0")` for project scopes generated by the concurrent solver,
       and `Scope("", "s_1-1")` for project scopes generated by the traditional solver.
    2. Add the project scope to the list of shared scopes in the exported library.
       Instead of `Library([], ...)`, this term should now look like `Library([Scope("/.", "s_prj-0")], ...)`.
    3. If it is present, *remove* the project root scope from the *second* list
       in the `Library` term.
    4. Remove the datum on the project scope. To do this, find the project scope
       entry in the scope graph, and change its second argument from `Some(...)`
       to `None()`. The entry should now roughly look like `(Scope("/.", "s_prj-0"), None(), [...])`.

The second step is to copy this file in the `lib/` directory of the project
that will use the library. Additionally, you might rename the file to something
more descriptive (e.g. `stdlib`), but ensure that the `.stxlib` extension is preserved.

Thirdly, the library must be enabled. To enable the library, create a `lib/stxlibs`
file (no extension) that contains a list of enabled library names. Continuing our
previous example, the content of that file would be `["stdlib"]`.

!!! warning "Project-level Declarations"
    When the *project constraint* asserts declarations, these will be duplicated,
    because the project constraint is solved both when analyzing the library and
    when analyzing the project using the library. As a general principle,
    project constraints *should not* make declarations. Instead, libraries are
    meant as a replacement for the project constraint to declare built-in types.

??? note "Multiple Libraries"
    Using multiple libraries is supported by adding multple `*.stxlib` files in
    the `lib/` directory, and having multiple entries in the `stxlibs` file. An
    example of such a file could look like `["lib1", "lib2"]`. Note however that
    libraries will not link properly when different exports are used, due to the
    fact that scope identities are not deterministic.

## Incremental Solver

Thirdly, there is experimental support for incremental analysis. To enable this,
the following options for the `mode`/`modes` settings are available:

- In language projects: `incremental-scope-graph-diff`.
- In example projects: `incremental-deadlock` or `incremental-scope-graph-diff`.
