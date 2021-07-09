
## Modules

A module is defined by a single flowspec file. A module can contain several sections, for defining control-flow, data flow, types, and functions. Modules can import other modules.

```
module $module-id

imports

    $module-ref*

$section*
```

## Terms and Patterns

FlowSpec defines various data types, including terms, tuples, sets, and maps. These can be constructed by the user, or introduced by matching on the AST.

```
term = ctor-id "(" {term ","}* ")"
     | "(" {term ","}* ")"
     | "{" {term ","}* "}"
     | "{" term "|" {term ","}* "}"
     | "{" {(term "|->" term) ","}* "}"
     | "{" term "|->" term "|" {(term "|->" term) ","}* "}"
```

Examples of these terms can be found in the Expressions subsection.


Control flow and data flow rules can use patterns to define which rules apply to which AST nodes.

```
pattern = ctor-id "(" {pattern ","}* ")"
  | "(" {pattern ","}* ")"
  | var-id "@" pattern
  | "_"
  | var-id
```

_Example._ The following shows an example of a pattern, matching a `VarDec` constructor with an `Int` child, binding some of the subterms.
```
VarDec(n, _, num@Int(i))
```

## Control Flow

The control-flow section contains the rules that define the control-flow for the subject language.

```
control-flow rules

    $control-flow-rule*
```

### Control Flow Rules

A control-flow rule consists of a pattern and a corresponding list of control-flow chains.

```
control-flow-rule = "root"? pattern "=" {cfg-chain ","}+
                  | "node" pattern

cfg-chain = {cfg-chain-elem "->"}+

cfg-chain-elem = "entry"
               | "exit"
               | variable
               | "node" variable
               | "this"
```

_Example._ Module that specifies how the control-flow for the `Add` AST node goes from the lhs, the rhs, and then to the `Add` itself. It also specifies that `Int` must have a node in the control-flow graph.
```
module control

control-flow rules

  node Int(_)
  Add(l, r) = entry -> l -> r -> this -> exit
```

### Root Rules

A root of the control-flow defines the start and end nodes of a control-flow graph. You can have multiple control-flow graphs in the same AST, but not nested ones. Each control-flow graph has a unique start and end node. A root control-flow rule introduces the start and end node. In other control-flow rules these nodes can be referred to for abrupt termination.

```
cfg-chain-elem = ...
               | "start"
               | "end"
```

_Example._ Module that defines control-flow for a procedure, and the return statement that goes straight to the end of the procedure.
```
module control

control-flow rules

  root Procedure(args, _, body) = start -> args -> body -> end
  Return(_) = entry -> this -> end
```

## Data Flow

### Properties

The data flow section contains definitions of the properties to compute, and the rules that define how these properties are computed.

```
properties

  property-definition*
```

A property has a name, and a corresponding lattice type. The result after analysis will be a lattice of this type for each node in the control-flow graph.

```
property-definition = name ":" lattice
```

_Example._ Lattice definition for a constant-value analysis.
```
properties

  values: Map[name, Value]
```

### Rules

The data flow rules specify how data should flow across the control-flow graph.

```
property rules

  property-rule*
```

```
property-rule = name "(" prop-pattern ")" "=" expr
prop-pattern = name "->" pattern
             | pattern "->" name
             | pattern "." "start"
             | pattern "." "end"
```

_Example._ A simple specification for a constant-value analysis.
```
property rules

  values(_.end) = Map[string, Value].bottom
  values(prev -> VarDec(n, _, Int(i))) = { k |-> v | (k |-> v) <- values(prev), k != n } \/ {n |-> Const(i)}
  values(prev -> VarDec(n, _, _))      = { k |-> v | (k |-> v) <- values(prev), k != n } \/ {n |-> Top()}
  values(prev -> _) = values(prev)
```

## Types

Algebraic datatypes can be defined for use within lattices definitions. Users can directly match these datatypes, or construct new values.

```
types

  type-definition*
```

An algebraic datatype consists of a constructor and zero or more arguments. 

```
name =
  ("|" ctor-id "(" {type ","}* ")")+
```

_Example._ The definition for an algebraic type `ConstProp` used in constant value analysis.

```
types
  
  ConstProp =
  | Top()
  | Const(int)
  | Bottom()
```

## Lattices

Lattices are the main data type used in data-flow analysis, because of their desirable properties. Properties (the analysis results) must always be of type lattice. FlowSpec contains some builtin lattice types, but users can also specify their own.

```
lattices

  lattice-definition*
```

Lattice definitions must include the following: the underlying datatype, a join operator (either least-upper bound or greatest-lower bound), a top, and a bottom.

```
name where
  type = type
  lub([name], name) = expr
  top = expr
  bottom = expr
```

_Example._ A lattice definition using the `ConstProp` above to define a `Value` type.

```
lattices
  Value where
    type = ConstProp
    bottom = Bottom()
    top = Top()
    lub(l, r) = match (l, r) with
      | (Top(), _) => Top()
      | (_, Top()) => Top()
      | (Const(i), Const(j)) => if i == j then Const(i) else Top()
      | (_, Bottom()) => l
      | (Bottom(), _) => r
```


## Functions

Functions make it possible to reuse functionality and avoid duplication of logic.

```
functions

  function-definition*
```

```
name([{(name ":" type) ","}+]) =
  expr
```

## Expressions

### Integers

Integer literals are written with an optional minus sign followed by one or more decimals.

Supported integer operations are:

- Addition [`+`]
- Subtraction [`-`]
- Multiplication [`*`]
- Division [`/`]
- Modulo [`%`]
- Negate [`-`]
- Comparison [`<`, `<=`, `>`, `>=`, `==`, `!=`]

### Booleans

Boolean literals true and false are available as well as the usual boolean operations:

- And [`&&`]
- Or [`||`]
- Not [`!`]

### Sets and Maps

Set and map literals are both denoted with curly braces. A set literal contains a comma-separated list of elements: `{elem1, elem2, elem3}`. A map literal contains a comma-separated list of bindings of the form key |-> value: `{ key1 |-> value1, key2 |-> value2 }`.

Operations on sets and maps include

- Union [`\/`]
- Intersection [`/\`]
- Set/map minus [`\`]
- Containment/lookup [`in`]

There are also comprehensions of the form `{ new | old <- set, conditions }` or `{ newkey |-> newvalue | oldkey |-> oldvalue <- map, condition }`, where new elements or bindings are gathered based on old ones from a set or map, as long as the boolean condition expressions hold. Such a condition expression may also be a match expression without a body for the arms. This is commonly used to filter maps or sets.


_Example._ The following are some examples of sets and maps.
```
// A map comprehension filtering the key n
{ k |-> v | (k |-> v) <- values(prev), k != n }

// A map literal
{n |-> Top()}

// A set comprehension filtering the value n
{ k | k <- live(prev), k != n }

// A set literal
{ n, "b", "foo" }
```

### Match

Pattern matching can be done with a match expression: `match expr with | pattern1 => expr2 | pattern2 => expr2`, where expr are expressions and pattern are patterns. Terms and patterns are defined at the start of the reference.

### Variables and References

Pattern matching can introduce variables. Other references include values in the lattice, such as `MaySet.bottom` or `MustSet.top`.

### Functions and Lattice Operations

User defined functions are invoked with `functionname(arg1, arg2)`. Lattice operations can be similarly invoked, requiring the type name: `MaySet.lub(s1, s2)`.

### Property Lookup

Property lookup is similar to a function call, although property lookup only ever has a single argument.

_Example._ The following property rule performs a set comprehension over the results of a property lookup, `live(prev)`, where the property `live` has been declared in the `properties` section, and `next` is bound in the pattern.
```
live(VarDec(n, _, _) -> next) = { k | k <- live(next), k != n }
```

### Term Positions

FlowSpec provides a builtin function that returns the position of a term: `position(term)`. This can be used to differentiate two terms from an AST that are otherwise equal.

## Lexical Grammar

### Identifiers

Most identifiers in FlowSpec fall into one of two categories, which we will refer to as:

    Lowercase identifiers, that start with a lowercase character, and must match the regular expression [a-z][a-zA-Z0-9]*.
    Uppercase identifiers, that start with an uppercase character, and must match the regular expression [A-Z][a-zA-Z0-9]*.

### Comments

Comments in FlowSpec follow C-style comments:

    // ... single line ... for single-line comments
    /* ... multiple lines ... */ for multi-line comments

Multi-line comments can be nested, and run until the end of the file when the closing */ is omitted.
