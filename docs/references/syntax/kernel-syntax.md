# Kernel Syntax

The rules from context-free and lexical syntax are translated into kernel syntax by the SDF3 normalizer.
When writing kernel syntax, one has more control over the layout between symbols of a production.

As part of normalization, among other things, SDF3 renames each symbol in the lexical syntax to include the suffix ``-LEX`` and each symbol in the context-free syntax to include the suffix ``-CF``.

For example, the two productions

```
lexical syntax

    BinaryConst = [0-1]+

context-free syntax

  Block.Block = "{" Statement* "}"
```

written in kernel syntax look like

```
syntax

    Block-CF.Block  = "{" LAYOUT?-CF Statement*-CF LAYOUT?-CF "}"
    BinaryConst-LEX = [0-1]+
```

Literals and character classes are lexical by definition, thus they do not need any suffix.
Note that each symbol in kernel syntax is uniquely identified by its full name including ``-CF`` and ``-LEX``.
That is, two symbols named ``Block-CF`` and ``Block`` are different, if both occur in kernel syntax.
However, ``Block-CF`` is the same symbol as ``Block`` if the latter appears in a context-free syntax section.

As mentioned before, layout can only occur in between symbols if explicitly specified.

For example, the production

```
syntax

    Block-CF.Block  = "{" Statement*-CF LAYOUT?-CF "}"
```

does not allow layout to occur in between the opening bracket and the list of statements.

This means that a fragment such as:

```
    {
      x = 1;
    }
```

would not be recognized as a block.