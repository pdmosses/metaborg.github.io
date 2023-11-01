---
title: "Statix"
---
# Statix — Static Semantics

Statix is a meta-language for the specification of _static semantics_ in Spoofax.

[:material-message-question: How-tos](../../howtos/statix/index.md){ .md-button }
[:material-file-cog: Reference](../../references/statix/index.md){ .md-button }
[:material-source-branch: Sources](#sources){ .md-button }


## Structure
Statix specifications are organised in [modules](modules.md). In Statix, programs, types and all other data are represented using [terms](terms.md). Type-checking a program is performed by solving a set of [constraints](basic-constraints.md) over terms. In addition to these built-in constraints, specification writers can define their [own constraints](rules.md).

Type-checking is closely related to, and strongly intertwined with, name resolution. For that reason, Statix has built-in support for modelling name binding patterns in the form of [scope graphs](scope-graphs.md). During type-checking, names can be resolved using [queries](queries.md).

When transforming programs using in [Stratego](../stratego), Statix specifications can be executed, and the results accesssed using the [Stratego API for Statix](stratego-api.md).

Statix has a special [test format](tests.md), which can be used for isolating issues in a specification, or in the Statix ecosystem.

!!! tip
    Readers with little or no familiarity with Statix are recommended to read the [Language Concepts](concepts.md) section first.


## Sources
The sources of the different Statix components can be found at:

- [:material-source-branch: statix.lang](https://github.com/metaborg/nabl/tree/master/statix.lang): Statix language specification
- [:material-source-branch: statix.runtime](https://github.com/metaborg/nabl/tree/master/statix.runtime): Statix runtime implementation
- [:material-source-branch: statix.solver](https://github.com/metaborg/nabl/tree/master/statix.solver): Statix solver implementation
