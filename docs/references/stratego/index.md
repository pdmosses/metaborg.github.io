# Stratego

The Stratego language caters for the definition of program transformations.

Transformations operate on the abstract syntax trees of programs.
Abstract syntax trees are represented by means of first-order [terms](terms/).
By using the [concrete syntax](concrete-syntax/) of a language, transformations can be expressed in the native syntax of the language under transformation, rather than using abstract syntax.

A program is structured as a collection of [modules](modules/), which may import each other.

Transformations are defined by means of named [rewrite rules](rewrite-rules/).
Rules may explicitly invoke rules.
Alternatively, rules may be invoked by [strategies](strategies/) that define how to combine rules into a more complex transformation using [strategy combinators](strategy-combinators/).
Context-sensitive transformations can be expressed using [dynamic rewrite rules](dynamic-rules/).

Starting with Stratego 2, terms and transformation strategies are (gradually) [typed](types/).



## Source

The sources of the Stratego implementation can be found at

- https://github.com/metaborg/stratego: The Stratego language implementation

- https://github.com/metaborg/strategoxt: The Stratego/XT ecosystem

!!! todo
    Give more specific links to syntax definition etc.
