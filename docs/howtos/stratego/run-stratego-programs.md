# How to Run Stratego Programs

Stratego programs that are part of a language project in Spoofax/Eclipse are run by creating a menu entry that invokes a strategy in your program.


## Extend Spoofax Menu

```esv
module $ModuleName
menus
  menu: "$Menu" (openeditor)
  action: "$MenuEntry" = $Id
```

Add a new ESV file in the `editor/` directory of your project or use an existing one.

In the `menus` section, create a menu with an appropriate name.
Adding the attribute `openeditor` ensures that the result of running the program will be opened in an editor.

Add an action entry to the menu with the name of the menu entry and the name of the builder strategy to invoke.

This should add a menu entry `Spoofax > Menu > Action` to the editor for your language.


## Define Builder

```stratego
$Id:
  (node, _, _, path, project-path) -> (filename, result)
  with filename := <guarantee-extension(|$Extension)> path
  with result   := <$Strategy>node
```

In your Stratego program, probably in some top-level file in the `trans/` directory of your project, add a 'builder' rewrite rule.
Such a rewrite rule defines the interface between the user-interface (action menu entry) and your program.

A builder has the interface shown above.
When invoking the builder, Spoofax takes care of parsing the program and converting it to abstract syntax term.
It takes a quintuple of the selected AST `node`, the entire `ast`, the file `path`, and the `project-path` and returns a pair of the `filename` and `result`.

The results are computed in the conditions of the builder rule.
The new `filename` is typically derived from the old file name in `path`
The `result` is computed by invoking a strategy on the selected `node` or on the entire `ast`.


## Example: Parser

```esv
module Syntax
//...
menus
  menu: "Syntax" (openeditor)
    action: "Show parsed AST" = debug-show-aterm (source)
```

```stratego
debug-show-aterm:
  (node, _, _, path, project-path) -> (filename, result)
  with
    filename := <guarantee-extension(|"aterm")> path
  ; result   := node
```

The `debug-show-aterm` provided with new Spoofax projects returns the selected `node` as result.
Since Spoofax ensures that the content of the editor is parsed, this returns the AST of the editor content as a (pretty-printed) term.


## Example: Term Builder

```esv
module Compilation
menus
  menu: "Compilation" (openeditor)
    action: "Desugar (AST)" = desugar-aterm
```

```stratego
rules

  desugar-aterm:
    (node, _, _, path, project-path) -> (filename, result)
    with filename := <guarantee-extension(|"d.aterm")> path
    with result   := <desugar>node
```

The `Desugar (AST)` menu action calls the `desugar-aterm` builder, which in turn uses the `desugar` strategy to transform the selected `node`.
The result is returned in a file with extension `d.aterm`.


## Example: Pretty Printing Builder

```esv
module Compilation
menus
  menu: "Compilation" (openeditor)
  action: "Desugar" = desugar-pp
```

```stratego
rules

  desugar-pp:
    (node, _, _, path, project-path) -> (filename, result)
    with filename := <guarantee-extension(|"d.tig")> path
    with result   := <desugar; pp-tiger-string>node  
```

The `Desugar` menu action calls the `desugar-pp` builder.
That strategy transforms the selected `node` with `desugar` and pretty-prints the resulting term with `pp-tiger-string`.
The result is returned in a file with extension `d.tig`.

## Define SPT Tests

An alternative way to run transformations is to test them using SPT tests.

This allows you to systematically run a transformation on a number of typical cases.


## Run On Save

When a Stratego program is applied in production, a transformation can be applied automatically whenever a program in your language is saved.
