# Modules

A Stratego program is organised as a collection of modules, which are imported from a main module.


## Module Structure

```stratego
module $ModuleName
$Imports*
$Section*
```

A module starts with a module header followed by a list of `imports`.
The name of a module in the header and imports should correspond to the file name, relative to a 'root' directory.

The rest of a module consists of `signature`, `rules`, and `strategies` sections, in any order, and possibly repeated.

## File Name and File Extension

A module coincides with the file it resides in. It is not possible to define more than one module in a file, which precludes nested modules.
The name of a module coincides with the file name, which should be fully qualified relative to a root directory.

A Stratego is a file with the extension `.str2` for Stratego 2.
Modules for the Stratego 1 version of the language have extension `.str`.
The file extension does not feature in the module names used in the language.

The following is example module header:

```stratego
module compilation/translation
imports desugaring/desugar
```

## Module Names

Module names can be hierarchical.
For example, consider the following directory structure

```
- trans
  - compilation
    - optimization.str2
    - translation.str2
  - desugaring
    - desugar.str2
```
A declaration of or reference to a module uses its fully qualified name, with `/` to indicate the directory structure, relative to a 'root' directory.

For example, if `trans` is [declared as a root](../config/index.md), then the module names for the modules above are

```
- compilation/optimization
- compilation/translation
- desugaring/desugar
```

## Imports

```stratego
imports $ModuleName+
```

A module should import all other modules from which it uses definitions.
Imports are non-transitive and may be mutually recursive.

Modules can extend rule and strategy definitions from other modules.
This allows the modular extension of a language.

When imported, all definitions in a module are visible.
There are currently no mechanisms for hiding definitions.

An `imports` can list multiple modules.
The form

```stratego
imports A B
```

is equivalent to

```stratego
imports A
imports B
```


## Signatures

A [signature](terms/types.md) section introduces sorts, constructors, and overlays.

```stratego
signature
  sorts $Sort*
  constructors
    $ConstructorDef*
  overlays
    $OverlayDef*
```

## Rules and Strategies

[Rule](rules/rewrite-rules.md) definitions and [strategy](strategies/strategy-definitions.md) definitions introduce named transformations.

```stratego
rules
  $RuleDef*
```

```stratego
strategies  
  $StrategyDef*
```

The `rules` and `strategies` section headers are indicative only; rule and strategy definitions can actually be mixed.

## Libraries

A Stratego library is a closed collection of modules.
A library can be pre-compiled since client programs may not extend its definitions.
A library is used by importing a collection of _external_ definitions of the signatures of constructors and transformations it defines.
Even if definitions in a library are not included in a libraries external definition, they cannot be redefined, as that produces link errors.

## Source Inclusion

!!! todo

## Concrete Syntax

When using [concrete syntax](rules/concrete-syntax.md) in a module, a `.meta` file accompanying the module indicates the parse table to use.
