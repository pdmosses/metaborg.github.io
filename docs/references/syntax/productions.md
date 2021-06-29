# Productions

The basic building block of syntax sections is the production.
The left-hand side of a regular production rule can be either just a symbol or a symbol followed by ``.`` and a constructor name.
The right-hand side consists of zero or more symbols.
Both sides are separated by ``=``:

    <Symbol>               = <Symbol>*
    <Symbol>.<Constructor> = <Symbol>*

A production is read as the definition.
The symbol on the left-hand side is defined by the right-hand side of the production.

Productions are used to describe lexical as well as context-free syntax.
Productions may also occur in priority sections, but might also be referred to by its ``<Symbol>.<Constructor>``.
All productions with the same symbol together define the alternatives for that symbol.

## Attributes

The definition of lexical and context-free productions may be followed by attributes that define additional (syntactic or semantic) properties of that production.
The attributes are written between curly brackets after the right-hand side of a production.
If a production has more than one attribute they are separated by commas.
Attributes have thus the following form:

```
    <Sort>               = <Symbol>* { <Attribute1>, <Attribute2>, ...}
    <Sort>.<Constructor> = <Symbol>* { <Attribute1>, <Attribute2>, ...}
```

The following syntax-related attributes exist:

-  ``bracket`` is an important attribute in combination with priorities.
   For example, the *sdf2parenthesize* tool uses the ``bracket``
   attribute to find productions to add to a parse tree before pretty
   printing (when the tree violates priority constraints). Note that
   most of these tools demand the production with a ``bracket``
   attribute to have the shape: ``X = "(" X ")" {bracket}`` with any
   kind of bracket syntax but the ``X`` being the same symbol on the
   left-hand side and the right-hand side. The connection with
   priorities and associativity is that when a non-terminal is
   disambiguated using either of them, a production rule with the
   ``bracket`` attribute is probably also needed.
-  ``left``, ``right``, ``non-assoc``, ``assoc`` are disambiguation
   constructs used to define the associativity of productions. See [Disambiguation](disambiguation/).
-  ``prefer`` and ``avoid`` are **deprecated** disambiguation constructs to define preference of one derivation over others. See [Disambiguation](disambiguation/).
-  ``reject`` is a disambiguation construct that implements language difference. It is used for keyword reservation. See [Disambiguation](disambiguation/).
