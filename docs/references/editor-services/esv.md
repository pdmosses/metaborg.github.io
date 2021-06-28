# ESV

The _Editor Service (ESV)_ language is a declarative meta-language for configuring the editor services of a language. For example, the following ESV code fragment configures the syntax highlighting for a language, based on the types of tokens:

```esv
module color

colorer

  keyword    : 153 51 153
  identifier : black
  string     : 177 47 2
  number     : 17 131 22
  operator   : black
  layout     : 63 127 95 italic
```


## Structure
ESV files end with the `.esv` extension, and are by convention placed in the `editor/` folder of a language project. Each ESV file defines a module for the file, followed by import statements and then the main configuration sections. Each section consists of a number of keys and values.

!!! note "Main File"
    By convention, the main ESV file of a language project must live at `editor/Main.esv` (default) or `editor/main.esv`. Other ESV files can be (transitively) imported from the main ESV file.


### Module Definition
An ESV file starts with a _module definition_ at the top of the file:

```esv
module $ModuleName
```

The module name is the filename of the ESV file without the exttension, and relative to the `editor/` directory. For example, the module `editor/mylang/Syntax.esv` would have the following module name:

```esv
module mylang/Syntax
```

!!! note ""
    Module names can only contains the alphanumeric characters  and dash, underscore, and period, and use the forward slash (`/`) as the path separator.

    Module names cannot be in parent directories, so `../Syntax` is not allowed.


### Imports
The _imports_ section is an optional section immediately following the module definition. When specified it is given as:

```esv
imports
    $Imports
```

For example, to import `editor/Syntax.esv` and `editor/Analysis.esv`:

```esv
imports
    Syntax
    Analysis
```

!!! note "Imports are transitive."

!!! note ""
    At most one imports section is permitted. When specified, the `imports` section cannot be empty.


### Configuration Sections
The main body of an ESV file consists of any number of configuration sections. An example of a configuration section is:

```esv
language
  line comment:  "//"
  block comment: "/*" "*/"
```

The configuration sections are hard-coded in the ESV language, but mostly use a consistent syntax for the keys and values.

The following configuration sections are currently defined:

<!-- Keep this list sorted: -->
- `colorer`
    - [Syntax Highlighting](syntax-highlighting.md)
- `language`
    - [Language File Extensions](file-extensions.md)
    - [Parsing](parsing.md)
    - [Analysis](analysis.md)
    - [On-Save Handlers](on-save.md)
    - [Stratego Strategies](stratego.md)
- `menus`
    - [Action menus](menus.md)
- `references`
    - [Hover Tooltips](hover.md)
    - [Reference Resolutions](reference-resolution.md)
- `views`
    - [Outline View](outline.md)

The following sections have been deprecated:

<!-- Keep this list sorted: -->
- `analysis`
- `builders`
- `completions`
- `folding`
- `outliner`
- `refactorings`
