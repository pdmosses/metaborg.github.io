# Types

[Terms](terms.md) provide a generic, untyped format to represent tree-structured data.
Stratego transformations can transform such data, but require at least that the arities of term constructors that are used in rules are declared.

Starting with Stratego 2, the types of terms and term transformations _may_ be declared _and_ checked in more detail[@SmitsV20].


## Signatures

```stratego
signature
  $SigSection*
```

A signature declares the shape of well-formed terms using sort declarations, constructor declarations, and overlays.


### Sorts

```stratego
sorts $Sort*
```

A sort is determined by an identifier and optionally has arguments.

A sort (or _type_) identifies a collection of well-formed terms.

Convention: Sort identifiers start with a capital letter.

### Constructors

```stratego
constructors
  $ConstructorDecl
```

A constructor declaration has the form

```stratego
$Constructor : $Sort * ... * $Sort -> Decl
```

and declares a constructor name, the sorts of the argument terms, and the sort of the constructed term.

Convention: Constructor identifiers start with a capital letter.

Example: The constructor declaration

```stratego
Assign : ID * Exp -> Stmt
```

defines the constructor `Assign` with input sorts `ID` and `Exp` and output sort `Stmt`.
Thus, if `x` and `e` are terms of sort `ID` and `Exp`, respectively, then `Assign(x, e)` is a term of sort `Stmt`.

When the list of argument sorts is empty the arrow can be omitted:

```stratego
$Constructor : Decl
```

Example: The constructor declaration

```stratego
True : Bool
```

defines that `True()` is a term of sort `Bool`.
Note that the parentheses are required.
The term `True` is a variable.

The Stratego1 compiler only checks the arity of constructor applications against the signature.
The Stratego2 compiler uses signature definitions to type check code if it has been given a type signature.

### Injections

An injection is a constructor without name and with a single argument.

```stratego
  : $Sort -> $Sort
```

Injections include an entire type as a subtype of another type without cluttering the tree structure.


### List Type

```stratego
List($Sort)
```

The type constructor `List(_)` is for typing homogenous lists.

Exmample. The type `List(Exp)` represents lists of expressions `Exp`.


### Polymorphic Types

Stratego2 supports user-defined polymorphic types.
That is, sorts can have parameters.

For example, the following signature defines the type of priority queues, polymorphic in the carrier type, in which the priority is determined by the length of the list.

```stratego
signature
  sorts PrioQ(*)
  constructors
    NilQ  : PrioQ(a)
    ConsQ : a * int * List(a) * PrioQ(a) -> PrioQ(a)
```

### Tuple Type

```stratego
($TermType * ... * $TermType)
```

Tuple terms can be typed in strategy types.
Currently, tuple types cannot be used in term signatures.


### Overlays

```stratego
overlays
  $OverlayDef
```

An overlay defines a term abbreviation.
An overlay definition has the form

```stratego
  $Constructor($ID, ..., $ID) = $Term
```

and defines that applications of the constructor should be expanded to the term.


## Transformation Types

```stratego
$Id($StrategyType, ... | $TermType, ...) :: $TermType -> $TermType
```

A _transformation type_ defines the signature of a transformation with name `$Id` with the types of its strategy arguments and term arguments, the type of the 'current term' to which the transformation is applied, and the type of the term that is returned, if the transformation succeeds.
Transformation types are declared in `rules` or `strategies` sections.

```stratego
$Id($StrategyType, ...) :: $TermType -> $TermType
```

When a transformation only has strategy parameters, the bar can be left out.

```stratego
$Id :: $TermType -> $TermType
```

When a transformation also has no strategy parameters, the parentheses can be left out as well.

### Strategy Type

```stratego
$TermType -> $TermType
```

The type of a transformation/strategy argument is an arrow from a term type to a term type.

Note that transformation strategies cannot be reified as terms.

### Type Dynamic

```stratego
?
```

Type _dynamic_, written `?`, represents the unknown type.

Stratego2 is a gradually typed language in order to facilitate the migration from (mostly) untyped Stratego1 code to typed Stratego2 code.
Furthermore, some patterns in Stratego cannot be typed statically.

When used as a strategy type `?` represents `? -> ?`.


### Type Casts

```stratego
///syntax of casts
```

!!! todo
    syntactic form

Gradual type systems allow a term with the dynamic type to be used in any place where a static type is required.
Stratego2 will insert a type cast at such a point to check at run time that the term is type-correct.
This way, a Stratego program halts execution in predictable places when a run time type error occurs.
There can be no run time type errors in fully statically typed code either, only at the boundary between dynamically and statically typed code.


### Type Preserving

```stratego
TP
```

A _type preserving_ transformation transforms _any_ type to itself (or fails).

In signatures, a type preserving transformation is indicated with `TP`.

Example. The type declaration

```stratego
topdown(s : TP) :: TP
```

declares that the `topdown` strategy is type preserving if its argument strategy is.

The type-checking for a type preserving transformation is very strict.
It should be in terms of other type preserving transformations, or match the input term to a specific type and return a term from that specific type.


### Is Type

```stratego
is($Sort)
```

Given the definition of a term sort `S`, the `is(S)` strategy checks whether a term is of sort `S` and fails if that is not the case.

Example. The strategy `<is(Exp)>t` checks that term `t` conforms to the signature of sort `Exp`.

The `is(S)` strategy uses the same mechanism as type casts for checking a term type at run time.


## References

\bibliography
