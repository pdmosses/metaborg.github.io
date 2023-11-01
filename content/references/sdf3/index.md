---
title: "SDF3"
---
# SDF3 — Syntax Definition Formalism

SDF3 is the third version of the Syntax Definition Formalism meta-language in Spoofax for defining the syntax of a language, which is used for both parsing an input into an Abstract Syntax Tree, and to provide syntax highlighting.  Through the use of _templates_ SDF3 can also be used to define a pretty-printer.

<!--[:material-message-question: How-tos](../../howtos/){ .md-button }-->
[:material-file-cog: Reference](../../references/sdf3/index.md){ .md-button }
[:material-source-branch: Sources](#sources){ .md-button }


## Structure 
An SDF3 syntax definition is structured as a collection of [modules](modules.md), which may import each other.  Each module defines a number of [symbols](symbols.md), which are the building blocks of [productions](productions.md).  Productions are defined for [lexical](lexical-syntax.md), [context-free](context-free-syntax.md), or [kernel](kernel-syntax.md) syntax.  [Start symbols](start-symbols.md) indicate the entry point of a syntax definition.

Grammars can be [disambiguated](disambiguation.md) by means of rejects, priorities, associativity, and restrictions, and permissive grammars are automatically generated for [error-recovery](recovery.md) parsing.  Handwritten recovery rules can be added to tweak recovery behavior.

SDF3 automatically generates a pretty-printer for [template](templates.md)-based productions, and provides additional constructs for the definition of [layout-sensitive](layout-sensitivity.md) languages.

Several aspects related to syntax definition and parsing can be [configured](configuration.md).


## Sources
The sources of the SDF3 language can be found at:

- [:material-source-branch: template.lang](https://github.com/metaborg/sdf/tree/master/org.metaborg.meta.lang.template): SDF3 language specification
