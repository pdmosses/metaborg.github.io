# Modules

An SDF3 specification consists of a number of module declarations. Each module defines sections and may import other modules.

## Imports

Modules may import other modules for reuse or separation of concerns. A module may extend the definition of a non-terminal in another module. A module may compose the definition of a language by importing the parts of the language. The structure of a module is as follows:

```
module <ModuleName>

<ImportSection>*

<Section>*
```

The ``module`` keyword is followed by the module name, then a series of imports can be made, followed by sections that contain the actual definition of the syntax. An import section is structured as follows:

```
imports <ModuleName>*
```

Note that SDF3 does not support parameterized modules.

## Sections

A SDF3 module may constitute of zero or more sections. All sections contribute to the final grammar that defines a language:

 - `sorts`, `lexical sorts`, `context-free sorts` (see [Sorts](sorts/))
 - `lexical syntax` (see [Lexical Syntax](lexical-syntax/))
 - `context-free syntax` (see [Context-Free Syntax](context-free-syntax/))
 - `syntax` (see [Kernel Syntax](kernel-syntax/))
 - `lexical start-symbols`, `context-free start-symbols`, `start-symbols` (see [Start Symbols](start-symbols/))
 - `context-free priorities`, `priorities` (see [Disambiguation](disambiguation/))
 - `template options` (see [Templates](templates/))
