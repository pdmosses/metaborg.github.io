# Modules

A Stratego program is organised as a collection of modules.

## File Extension

A Stratego is a file with the extension `.str2` for Stratego 2.

Modules for the Stratego 1 version of the language have extension `.str`.

## Module Names

Module names can be hierarchical

For example, consider the following directory structure

```
- trans
  - compilation
    - optimization.str2
    - translation.str2
  - desugaring
    - desugar.str2
```

If `trans` is declared as a root, then the module names are

```
- trans
  - compilation
    - compilation/optimization
    - compilation/translation
  - desugaring
    - desugaring/desugar
```

!!! check
    terminology


## Module Structure

A Stratego module has the following structure, where a single occurrence of a construct can actually be multiplied:

```stratego
module $FileName

imports $FileName

rules

  $RuleDef

strategies

  $StrategyDef
```

## Imports

A module should import all other modules from which it uses definitions.

Imports are non-transitive

modules can extend definitions

## Libraries

pre-compiled libraries 

external definitions



## Concrete Syntax

To use [concrete syntax](concrete-syntax/) define a `.meta` file to accompany the module.
