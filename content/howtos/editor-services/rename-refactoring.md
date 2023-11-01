# Add Rename Refactoring to an Existing Project
[Rename Refactoring][1] is the ability for the user to select a reference or declaration and rename it to across the whole program while not introducing errors and not touching syntactically equal names.

## Renaming in Statix
To enable the Rename Refactoring for an existing Spoofax Language project that uses Statix, create an action that calls the `rename-action` strategy from the `statixruntime` library. The parameters are explained in [the reference][1]. For example:

```stratego
module renaming

imports
  statixruntime
  statix/runtime/renaming

  pp
  analysis

rules
  rename-menu-action = rename-action(construct-textual-change,
    editor-analyze, id)
```

## Renaming in NaBL2
There also exists a version of the Rename refactoring that works with languages using NaBL2. It can be added with a Stratego module like this:

```stratego
module renaming

imports
  nabl2/runtime

  pp
  analysis

rules
  rename-menu-action = nabl2-rename-action(construct-textual-change,
    editor-analyze, id)
```

## Menu Action
The rename refactoring is triggered from an entry in the Spoofax menu. To add it to an existing project a menu like the following can be implemented in an [ESV file](../../references/esv/index.md):

```esv
module Refactoring

menus
  menu: "Refactoring"
    action: "Rename" = rename-menu-action
```

## See Also
- Reference: [Rename Refactoring][1]


[1]: ../../references/editor-services/renaming.md