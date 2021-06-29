# Start Symbols

The lexical or context-free start symbols sections explicitly define the symbols which will serve as start symbols when parsing terms.
If no start symbols are defined it is not possible to recognize terms.
This has the effect that input sentences corresponding to these symbols can be parsed.
So, if we want to recognize boolean terms we have to define explicitly the sort ``Boolean`` as a start symbol in the module ``Booleans``.
Any symbol and also lists, optionals, etc., can serve as a start-symbol.
A definition of lexical start symbols looks like:

```
lexical start-symbols

    $Symbol*
```

While context-free start symbols are defined as:

```
context-free start-symbols

    $Symbol*
```

SDF3 also supports kernel start-symbols:

```
start-symbols

    $Symbol*
```

In contrast to lexical and kernel start-symbols, context-free start symbols can be surrounded by optional layout.
A lexical start-symbol should have been defined by a production in the lexical syntax; a context-free symbol should have been defined in the context-free syntax.
Both symbols can also be defined in kernel syntax using the suffix ``-LEX`` or ``-CF``.
