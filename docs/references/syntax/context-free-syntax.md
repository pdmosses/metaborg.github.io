# Context-Free Syntax

The context-free syntax describes the more high-level syntactic structure of sentences in a language.
A context-free syntax contains a list of productions.
Elements of the right-hand side of a context-free production are pre-processed in a normalization step before parser generation that adds the ``LAYOUT?`` symbol between any two symbols.

Context-free syntax has the form:

```
context-free syntax

  <Production>*
```

An example production rule:

```
context-free syntax

  Block.Block = "{" Statement* "}"
```

SDF3 automatically allows for layout to be present between the symbols of a rule.
This means that a fragment such as:

```
{

}
```

will still be recognized as a block (assuming that the newline and line-feed characters are defined as layout).
