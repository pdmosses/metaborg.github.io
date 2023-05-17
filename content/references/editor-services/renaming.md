# Rename Refactoring

Spoofax provides an automated _rename refactoring_ as an editor service for every language developed with it that has the static semantics defined with Statix or NaBL2.

## Strategy
Rename refactoring is enabled by default for new Spoofax language projects. This works by registering the `rename-action` strategy from the `statixruntime` library as an action in a menu. This strategy takes three parameters: a layout-preserving pretty-printing strategy (`construct-textual-change` by default), the editor analyze strategy (`editor-analyze` by default), and a strategy that should succeed when renaming in multi-file mode.

The default rename refactoring strategy looks like this:

```stratego
rules

  rename-menu-action = rename-action(construct-textual-change,
    editor-analyze, fail)
```

To enable multi-file mode, change the last argument to `id`:

```stratego
rules

  rename-menu-action = rename-action(construct-textual-change,
    editor-analyze, id)
```


## Statix
For the renaming to work correctly in all cases when using Statix, terms that represent a declaration of a program entity, such as a function or a variable, need to set the `@decl` property on the name of the entity. For example, when declaring a type:

```statix
declareType(scope, name, T) :-
  !type[name, T] in scope,
  @name.decl := name,
  query type filter P* I* and { name' :- name' == name } in scope |-> [_].
```


## Known Issues

When a parse tree of a name is preceded by a term which is parsed from an empty
string. The renaming algorithm will incorrectly select the preceding term to be
renamed, and mostly fail accordingly. Sometimes, this issue can be circumvented
by selecting the complete surrounding term. This issue is known to occur for:

- Statix predicate names.

## See Also
- How-To: [Add Rename Refactoring to an Existing Project](../../howtos/editor-services/rename-refactoring.md)
