# Outline View
An outline is a summary of the structure of a file, shown in a separate view next to a textual editor. An outline is created by a Stratego strategy, but is configured in an [ESV file](esv.md) under the `views` section:

```esv
views

  outline view: $Strategy
    expand to level: $Int
```

The Stratego strategy specified as `$Strategy` must have the following signature:

```stratego
signature
  constructors
  
    Node : Label * Children -> Node

rules
  
  editor-outline:
    (node, position, ast, path, project-path) -> outline
```

Where the input is the default tuple used for [_builders_](menus.md), and the result is a list of `Node` terms, each carrying a label and a (possibly empty) list of child nodes.

!!! note ""
    Preserve origins on the node's label to allow navigating to the corresponding code from the outline.

For example:

```esv
views

  outline view: editor-outline
    expand to level: 3
```

This configures the `editor-outline` Stratego strategy to be used to create outlines, and that outline nodes should be expanded 3 levels deep by default.
