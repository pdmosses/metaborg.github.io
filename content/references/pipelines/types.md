# Types

This page explains the type system of the PIE DSL and lists all the built-in types.

## The type system

A type system checks for type errors.
PIE DSL uses a static type system, so type errors are found before compilation.
The PIE DSL supports subtypes, generics and methods on types.

### Nullability

PIE DSL keeps explicit track of nullability, so an expression cannot be null unless [the type of the expression is nullable](#nullable-types).

!!! todo
    Fully document nullability.

### Super types and subtypes

When a type `X` is a subtype of type `Y`, you can use an expression with type `X` wherever an expression with type `Y` is expected.
When `X` is a subtype of `Y`, `Y` is the super type of `X`
For example, the method `cutFruit(fruit: Fruit) -> Piece*` expects a `Fruit`.
If an `Apple` is declared to be a subtype of `Fruit`, we can pass an `Apple`: `cutFruit(getApple())`

Subtypes are transitive, which means that if `A` is a subtype of `B`, and `B` is a subtype of `C`, then `A` is a subtype of `C`, even if that is not explicitly declared.

The PIE DSL allows declaring exactly one super type.

The top type is a super type of everything.
As such, any expression can be assigned to the top type.

The bottom type is a subtype of everything.
As such, an expression with the bottom type can be assigned to everything.


### Generics

Generics refer to making a type or a function generic over types, that is, add type parameters to the type or function.
You likely already know about these, lists are an example of parameterized types.
It's not just any list, it's a list of `some type here`.

Every data type in the PIE DSL is generic.
When declaring a datatype in a data definition, there is a list of generic parameters: `data Box<T> = $DataImpl`.
When referring to a type, there is a list of generic parameters:
`val box: Box<string> = $Exp`.
These lists can be empty: `data Apple<> = $DataImpl`.
This makes the term "generic" a bit meaningless, but `Apple` is still considered generic for the purposes of the semantics.
That is to say, `Apple` is treated as a generic type that just happens to have zero generic parameters, in the same way that `Box` happens to have one generic parameter and `Foo<A, B, C>` happens to have three.

??? tip "Omitting type parameter and argument lists"
    Type parameter/argument list can sometimes be omitted.
    Parameter lists can be omitted if they are empty: `data Apple = $DataImpl`, `func notGeneric(string) -> unit = $FuncImpl`.
    Type argument lists can be omitted for empty lists and for calls to [the built-in `supplier` function](../expressions#create-supplier).
    For example, `Apple`, `notGeneric("regular argument")`.

A type declares zero or more generic parameters.
These can be used in methods of that type to parameterize the method.

A function or method can also declare generic parameters to be used in that function or method.

??? note "PIE does not derive bounds"
    Unlike Java, the PIE DSL does not derive bounds for datatypes based on super types.
    The following would be possible in Java but will not work in the PIE DSL:
    ```
    data CustomAnimalSet<A : Animal> = $DataImpl
    data OrderedAnimalSet<T> : CustomAnimalSet<T> = $DataImpl
    // error on `T` in `CustomAnimalSet<T>`: `T` is not within upper bound `Animal`
    // Solution: declare the bound on the subtype as well
    data OrderedAnimalSet2<T : Animal> : CustomAnimalSet<T> = $DataImpl
    ```

!!! todo
    Explain generics

### Methods and overriding

Every type can have methods.
For now, the only data types are `foreign java` datatypes, so methods follow Java semantics for overriding.

!!! todo
    Explain overriding.


## Built-in types

The PIE DSL has several built-in types.
This section explains all of them.

??? note "Datatype equality with equal Java class"
    PIE DSL does not consider types equivalent when their backing Java class is equal.
    This means that a built-in type and a custom datatype backed by the same class cannot be used interchangeably.

The following table gives a quick overview of the built-in types, click on the name to go to the documentation.

| name | syntax | description | values | methods | backing Java class |
| --- | --- | --- | --- | --- | --- |
| [unit](#unit) | `unit` | Unit type, only has a single value. Use as return type for methods without a meaningful return value | `unit` | - | `mb.pie.api.None` |
| [bool](#bool) | `bool` | Booleans. Used as flags and for conditions in `if` and `if-else`. | `true`, `false` | - | `java.lang.Boolean` |
| [int](#int) | `int` | Integers. Range from $-2^{31}$ to $2^{31}-1$, inclusive. | -2147483648, ... -1, 0, 1, 2, 3, ... 2147483647 | - | `java.lang.Integer` |
| [path](#path) | `path` | Paths on the file system. Might not exist. | E.g. `./src/test/resources/test1.txt`, `/home/users/me/programming` | - | `mb.resource.fs.FSPath` |
| [null type](#null-type) | - | Type of the literal `null`. Subtype of every [nullable type](#nullable-types). | `null` | - | - |
| [top](#top) | - | The top type is the super type of all other types. | every value is an instance of `top` | - | `java.lang.Object` |
| [bottom](#bottom) | - | The bottom type is a subtype of all other types. It has no values by definition. An expression of type bottom will never return normally. | No values | - | - |
| [Nullable types](#nullable-types) | `$Type?`, e.g. `string?` | Makes a type nullable. | All values of the original type and `null` | All methods of the original type | Original backing class |
| [Lists](#lists) | `$Type*`, e.g. `int*` | A list. Unknown amount of elements, all with the same type. | `[]`, `[e1]`, `[e1, e2]`, `[e1, e2, e3]`, where `e1`, `e2` and `e3` are valid elements of the list element type. | - | `java.util.ArrayList` |
| [Tuples](#tuples) | `($Types)` | A tuple of elements. Known amount of elements, can be different types. | elements of the inner types, e.g. `(e1, e2)` is a value of `(T1, T2)` if `e1` and `e2` are values of `T1` and `T2` respectively | - | `mb.pie.TupleX`, where `X` is the number of elements. |
| [supplier](#supplier) | `supplier<$Type>` | A supplier of a value. Useful for performance in certain situations. | Can be created using `supplier($Exp)` or `$FUNCID.supplier<$TypeArgs>($Exps)` | `func get<>() -> T` for `supplier<T>` | `mb.pie.api.Supplier` |
| [Function types](#function-types) | - | The type of a function. Functions cannot be used as values, but their type can be seen by hovering over the name | - | - | - |
| [Wildcards](#wildcards) | `_$UpperBound$LowerBound` | Represent a set of types. Can only be used as type argument. | Instances of types in the type set | - | Backed by the Java wildcard: `?` |
| [Custom datatypes](#custom-datatypes) | `$TYPEID` | A type defined in a pie file with. | Instances of the type, ultimately obtained from `foreign java` functions | The methods that are declared on the type itself, and the methods of its super types | The declared backing class |


### unit
`unit` is a type with only a single value: `unit`.
It is meant to be used as return value for functions that have no meaningful return value, for example functions that operate via side effects like writing to a file.
It is backed by `mb.pie.api.None`.


### bool
`bool` represents booleans and as such has two values: `true` and `false`.
Booleans are used as flags and as conditions for `if` and `if-else`.
`bool` is backed by `java.lang.Boolean`.


### int
`int` represents integers.
It is backed by `java.lang.Integer`, and as such has a range of $-2^{31}$ to $2^{31}-1$, inclusive.


### string
`string` represents strings.
Strings have many built-in methods which have yet to be added to the implementation.
It is backed by java `String`.


### path
`path` represents a path to a file or directory in the file system.
The directory or file need not exist.
Paths can be relative or absolute.
Paths have many built-in methods which have yet to be added to the implementation.
Paths are backed by `mb.resource.fs.FSPath`


### null type
The null type cannot be expressed in the PIE DSL, meaning that there is no way to specify it as the type of something.
Its only value is `null`.
The null type is a subtype of every nullable type.


### top
The top type is a super type of every other type.
It cannot be specified as a type.
It is backed by `java.lang.Object`


### bottom
The bottom type is a subtype of every other type.
It cannot be specified as a type.
The bottom type has no values, and as such an expression with bottom type will never return normally to the function it is defined in.
It is the element type of empty lists, and in the future also of `return` and `fail` expressions.
This type is not backed by any java class.
???+ failure "Compiling bottom type"
    Code that has the bottom type will fail to compile.
    Remove the code that has bottom type to resolve this.


### Nullable types
Nullable types are represented with a question mark after the type.
For example, a nullable `int` is `int?`.
A nullable type `X?` represents a value that could either be a regular value `X` or "missing", represented with the expression `null`.
A nullable type `X?` is a super type of both `X` and the null type.
It is an error to make a nullable type nullable again, so `X??` is not allowed.
Java types are always nullable, so the nullable type `X?` is backed by Java type `X`.


### Lists
Lists are represented with an asterisk behind the type.
For example, a list of `path` is `path*`.
Lists of `X` can contain any element that could be assigned to `X`.
Lists do not have subtypes besides the bottom type.
This means that `Apple*` is not a subtype of `Fruit*`.
Lists do not have methods yet.
Lists are backed by Java `java.util.ArrayList`.

??? info "Empty lists"
    The PIE DSL type system keeps track of empty lists for implementation reasons.
    Because it is doing this anyway, it gives warnings when doing certain non-sensical things such as appending an empty list to another list or list comprehension over empty lists.


### Tuples
Tuple types represent a combination of multiple types.
They are specified as the types between parentheses.
For example, `(string, int*)` represents a pair of a `string` and a list of `int`s.
Tuple types differ from lists because lists have a variable amount of elements of a single type, while tuples have a set number of elements with heterogenous types.
Tuple types can be deconstructed to get their values:
```PIE
val pair: (string, int*) = ("Alice", [9, 4, 6, 7]);
val (name: string, grades: int*) = pair;
```
Tuples are backed by Java classes `mb.pie.TupleX`, where `X` is a number representing the amount of elements, e.g. `Tuple2` for a pair.
This is because Java is not generic in the amount of generic elements.

???+ attention "Limits on tuple sizes"
    While the PIE DSL language does not specify a limit on the amount of elements in a tuple, the backing Java `TupleX` classes only go up to 10.
    If you run into this limit, use a foreign data type backed by a custom Java class instead.


### supplier
`supplier<T>` represents a supplier of a value of type `T`.
Suppliers represent a value, either by [being created with a value](../expressions#create-supplier) or by [deferring a task that returns the value](../expressions#task-supplier).
Suppliers have a single method `get<>() -> T`, which returns the value of the supplier, either by returning the value if it already existed or by calling the task that the supplier supplies.

The main use case for suppliers is as input types for tasks.
If the supplier is faster to check for consistency than the value it supplies, the runtime performance is improved.
As an example, consider
```PIE
func readFile() -> string = read ./bundled.java

func parse1(program: string) -> IStrategoTerm =
  mb:lang:java:parse(program)
func parse2(program: supplier<string>) -> IStrategoTerm =
  mb:lang:java:parse(program.get<>())

func parseBoth() -> unit = {
    parse1(readFile());
    parse2(readfile.supplier());
    unit
}
```
Both `parse1` and `parse2` need to read the file `./bundled.java`, strip of any whitespace, and then parse it with `mb:lang:java:parse` on the initial build.
If we modify `./bundled.java` before the second build, `readFile` is now outdated and will need to read again.
To check if the input for `parse1` is in the cache, the runtime needs to check the contents of the entire file against any cached values to see if it matches.
To check if the input for `parse2` is in the cache, the runtime only checks if the supplier is in the cache.
The supplier is a `TaskSupplier`, which is in the cache if its task is not outdated.
The runtime only has to make a few calls to determine that the input for `parse2` is not cached.

Suppliers are backed by `mb.pie.api.Supplier`.

### Function types
Function types are visible when hovering over a function name.
They follow the pattern `func($Params) -> $Type`.
For example, `func(int, string) -> bool` is a function that takes an int and a string and returns a boolean.
Function types cannot be specified in PIE DSL, and they can also not be the type of a variable.
Because function types cannot be the type of a variable, they are not backed by a Java class.


### Wildcards
Wildcards represent a set of types by using an upper or lower bound.
They use the following syntax.
The wildcard itself is represented by an underscore: `_`
The upper bound is specified by a colon followed by a type: ` : $Type`
The lower bound is specified with a dash, colon and then a type: ` -: $Type`
If a the upper bound is omitted, it is implicitly the top type.
If the lower bound is omitted, it is implicitly the bottom type.
A wildcard cannot have both an upper and a lower bound.

Here are some examples of wildcards and what they mean:
```PIE
_ // unbounded wildcard (bounds are implicitly the top and bottom type)
_ : Fruit // upper bounded wildcard. Matches Fruit, Apple, Pear
_ : path:to:module:Vegetable // qualified upper bound
_ -: Fruit // lower bounded wildcard. Matches Fruit, Food, top type

_ : Fruit -: Apple // both upper and lower bounded, gives an error

_ : Iterable : Comparable // _not_ a type with multiple upper bounds, parsed as
_ : Iterable:Comparable   // a single qualified upper bound.

_ -: Apple : Fruit // _not_ a lower bound and then upper bound, parsed as
_ -: Apple:Fruit   // a qualified lower bound
```

Wildcards can only be used as type arguments or as arguments to built-in types.
They are useful when we want to allow any of the type arguments within the bounds.
For example, `func buildZoo(Animal*) -> Zoo` will only take a list with type `Animal*`, but not a list with type `Mammal*`, even though a zoo of just mammals can be pretty cool already.
To allow any list of animals, we use a wildcard: `func buildZoo((_ : Animal)*) -> Zoo`
This `buildZoo` will take `Animal*`, `Mammal*`, `Bird*`, `Insect*` and even `Chicken*`.

Wildcards are translated to Java wildcards.


## Custom datatypes
Custom datatypes are definitions using the `data` keyword.
They look like this:
```PIE
$Modifiers data $TYPEID<$GenericParameters> : $SuperType = $DataImpl

$Modifier = "transient"
$DataImpl = foreign java $QID {
    $FuncHeads
}
```

Modifiers change the semantics of a datatype.
The only modifier right now is `transient`.
This modifier signifies to the PIE runtime that the datatype cannot be cached.
It is an error to repeat modifiers, i.e. `transient transient data Foo = $DataImpl` is not allowed.

The name can be any name that not already a built-in type.
The convention is to use PascalCase, meaning that every first letter of a word is a capital letter.
Names start with a letter or underscore, and can contain letters, numbers, a dash (`-`) and underscores (`_`).

The list of generic parameters can be omitted.
This is syntactic sugar for an empty list, so `Foo` is the same as `Foo<>`.
For an explanation of generics in the PIE DSL, see [generics](../generics/)

The super type specifies the super type of this data type.
The super type can be omitted, for example `data Foo = $DataImpl`.
If the super type is omitted, the top type implicitly becomes the super type.
See [the section about super types and subtypes earlier on this page](#super-types-and-subtypes) for an explanation of super types.

The only implementation right now is `foreign java`.
This implementation is a Java class.
It looks like this
```PIE
foreign java $QID {
    $FuncHeads
}
```
The `$QID` specifies the qualified name of the backing Java class.
`$FuncHeads` is a newline separated list of function headers.
These are declarations of the non-static methods of the class.
Not all non-static methods of the class need to be declared here.
Static methods of the class can be declared as [`foreign java` functions](../functions#foreign-java-functions) outside this data definition.

???+ tip "Separate your imports"
    Define foreign java datatypes in a separate module and import them into your main module to keep your main module cleaner.
