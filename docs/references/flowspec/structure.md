## Structure

### Modules

A module is defined by a single flowspec file. A module can contain several sections, for defining control flow, data flow, types, and functions. Modules can import other modules.

```
module _module-id_

imports

    _module-ref*_

_section*_
```

### Control Flow

The control flow section contains the rules that define the control flow for the sorts in the subject grammar.

```
control-flow rules

    control-flow-rule*
```

#### Control Flow Rules

```
pattern* = {cfg-edges ","}+

cfg-edges = {cfg-edge-end "->"}+

cfg-edge-end = "entry"
             | "exit"
             | variable
             | "node" variable
             | "this"
```

_Example._
```
module control

control-flow rules

  node Int(_)
  Add(l, r) = entry -> l -> r -> this -> exit
```

#### Root Rules

### Data Flow

#### Properties

#### Rules

### Lattices

### Types

### Expressions

#### Literals

#### Sets and Maps

- Literals
- Union, Diff, Contains, Intersect
- Comprehension

#### Match

#### Variables and References

#### Functions

#### Property Lookup

#### Term Positions

#### Lattices

- Lattice operations

### Functions

### Lexical Grammar
