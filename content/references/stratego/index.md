---
title: "Stratego"
---
# Stratego — Term Transformations

The Stratego term transformation language caters for the definition of program transformations.

[:material-message-question: How-tos](../../howtos/stratego/index.md){ .md-button }
[:material-file-cog: Reference](../../references/stratego/index.md){ .md-button }
[:material-source-branch: Sources](#sources){ .md-button }


## Structure
Transformations operate on the abstract syntax trees of programs.
Abstract syntax trees are represented by means of first-order [terms](terms.md).

A program is structured as a collection of [modules](modules.md), which may import each other.

Transformations are defined by means of named [rewrite rules](rewrite-rules.md).
Rules may explicitly invoke rules.
Alternatively, rules may be invoked by [strategies](strategy-definitions.md) that define how to combine rules into a more complex transformation using [strategy combinators](strategy-combinators.md).
Context-sensitive transformations can be expressed using [dynamic rewrite rules](dynamic-rules.md).

Starting with Stratego 2, terms and transformation strategies are (gradually) [typed](types.md).


## Placeholder Convention
In this reference manual we use placeholders to indicate the syntactic structure of language constructs.
For example, a rewrite rule has the form

```stratego
$Label :
  $Term -> $Term
```

in which the `$Label` is the name of the rule, the first `$Term` the left-hand side, and the second the right-hand side of the rule.
This convention should give an indication of the formal structure of a construct, without going down to the precise details of the syntax definition.
As a side effect, the schema also shows the preferred indentation of language constructs where that is applicable.


## Not in Reference Manual

### Concrete Syntax  
By using the [concrete syntax](../../howtos/stratego/concrete-syntax.md) of a language, transformations can be expressed in the native syntax of the language under transformation, rather than using abstract syntax.


### Library
The Stratego standard library is a collection of modules that are available with each Stratego program and on which the runtime library relies.

Find automatically generated documentation at the following sites:

- http://releases.strategoxt.org/docs/api/libstratego-lib/stable/docs/
- https://stratego.martijndwars.nl/


## Sources
The sources of the different Stratego components can be found at:

- [metaborg/stratego :material-source-branch: stratego.lang](https://github.com/metaborg/stratego/tree/master/stratego.lang): Stratego language specification
- [metaborg/stratego :material-source-branch: strategolib](https://github.com/metaborg/stratego/tree/master/strategolib): Stratego core library
- [metaborg/strategoxt :material-source-branch: *](https://github.com/metaborg/strategoxt): Stratego/XT ecosystem

