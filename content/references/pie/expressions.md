# Expressions

Function bodies in PIE DSL consist entirely of expressions.
Every expression has a type and returns a value of that type, with the exception of `fail` and `return`.

Expressions can use brackets to override the default priority rules, for example `a && (b || c)`.
Brackets have the following form: `($Exp)`

This section describes expressions in the PIE DSL.
Expressions can use declared values.
These are described [in this section of the functions documentation](../functions#parameters-and-values).


## Syntactic priorities (disambiguation)

Nested expressions can be ambiguous, for example `! true && false` could either `! (true && false) // = true` or `(!true) && false // = false`.
To solve these ambiguities, each expression has a priority.
Expressions with higher priories will be nested in expressions with lower priority.
The example above is parsed as `(!true) && false` because [not](#not) has a higher priority than [logical and](#logical-and).
All expressions are left-associative, which means that if two expressions with the same priority are ambiguous, the leftmost expression will be nested in the rightmost expression.
For example, `3 - 2 + 1` is equivalent to `(3 - 2) + 1`.

The following list lists expressions in order of descending priority.
Expressions on the same number have the same priority.
If an expression is not listed, it cannot be ambiguous (e.g. Blocks and list literals)


<ol reversed>
    <li><a href="#not">Not</a></li>
    <li><a href="#make-nullable">Make nullable</a>, <a href="#make-non-nullable">Make non-nullable</a></li>
    <li><a href="#addition">Addition</a></li>
    <li><a href="#compare-for-inequality">Compare for (in)equality</a></li>
    <li><a href="#logical-and">Logical and</a></li>
    <li><a href="#logical-or">Logical or</a></li>
    <li><a href="#list">list</a>, <a href="#walk">walk</a></li>
    <li><a href="#requires">requires</a>, <a href="#generates">generates</a></li>
    <li><a href="#read">read</a>, <a href="#exists">exists</a></li>
    <li><a href="#function-calls">Function calls</a>, <a href="#method-calls">Method calls</a>, <a href="#create-supplier">Create supplier</a>, <a href="#task-supplier">Task supplier</a></li>
    <li><a href="#filter-and-filterpart">Filters</a></li>
    <li><a href="#tuple-literal">Tuple literal</a>, <a href="#list-literal">List literal</a></li>
    <li><a href="#list-comprehension">List comprehension</a></li>
    <li><a href="#value-declaration">Value declaration</a></li>
    <li><a href="#return">return</a>, <a href="#fail">fail</a></li>
    <li><a href="#if-else">if-else</a></li>
    <li><a href="#if">if</a></li>
</ol>


## Quick overview

The following table gives a quick overview of all expressions in the PIE DSL.

| name | syntax | example | description | type |
| ---- | ------ | ------- | ----------- | ---- |
| [Block](#block) | `{$Exps}` | `{val x = 4; x+7}` | A sequence of expressions | The type of the last expression |
| [Make nullable](#make-nullable) | `$Exp?` | `"nullable string"?` | Makes the type `T` of an expression [nullable](../types#nullable-types) (`T?`) | When applied to an expression of type `T`, `T?` |
| [Make non-nullable](#make-non-nullable) | `$Exp!` | `input!` | Makes the type `T?` of an expression non-[nullable](../types#nullable-types) (`T`). Throws an exception if the value is [null](#null) | When applied to an expression of type `T?`, `T` |
| [Not](#not) | `!$Exp` | `!flag` | Turns `false` to `true` and vice versa | [bool](../types#bool) |
| [Compare for (in)equality](#compare-for-inequality) | `$Exp == $Exp` and `Exp != $Exp` | `result == null`, `errors != []` | Compares two values for (in)equality | [bool](../types#bool) |
| [Logical or](#logical-or) | `$Exp || $Exp` | `dryRun || input == null` | Is `true` unless both the values are `false` | [bool](../types#bool) |
| [Logical and](#logical-and) | `$Exp && $Exp` | `!dryRun && input != null` | Is `true` iff both values are `true` | [bool](../types#bool) |
| [Addition](#addition) | `$Exp + $Exp` | `x + y` | Adds or concatenates two values | Depends on the types of the expressions |
| [Value declaration](#value-declaration) | `val $VALID TypeHint? = $Exp` | `val num: int = 47` | Declare a value by name | The type of the declared value |
| [Value reference](#value-reference) | `$VALID` | `x` | Reference a value or parameter | The type of the referenced value |
| [if](#if) | `if ($Exp) $Exp` | `if (input == null) fail "Input is null"` | Evaluates the body if the condition evaluates to `true` | [unit](../types#unit) |
| [if-else](#if-else) | `if ($Exp) $Exp else $Exp` | `if (name != null) name else default` | Evaluates the first branch if the condition is `true`, and the second branch otherwise | The least upper bound of the types of the branches |
| [List comprehension](#list-comprehension) | `[$Exp | $Binder <- $Exp]` | `["Key: $key; value: $value" | (key, value) <- pairs]` | Evaluate the expression for each element in a list | A [list](../types#lists) of the type of the expression |
| [Function calls](#function-calls) | `$ModuleList$FUNCID$TypeArgs($Exps)` | `stdLib:okResult<string>("Hello world!")` | Call [a function](../functions#function-invocations) | The [return type of the function](../functions#return-type) |
| [Method calls](#method-calls) | `$Exp.$FUNCID$TypeArgs($Exps)` | `file.replaceExtension("pp.pie")` | Call [a method](../functions#function-invocations) | The [return type of the method](../functions#return-type) |
| [Create supplier](#create-supplier) | `supplier$TypeArgs($Exps)` | `supplier(47)` | Create a supplier | [A supplier](../types#supplier) of the provided type |
| [Task supplier](#task-supplier) | `$ModuleList$FUNCID.supplier$TypeArgs($Exps)` | `lang:java:parse.supplier(file)` | Create a supplier from a function | [A supplier](../types#supplier) of the return type of the function |
| [requires](#requires) | `requires $Exp $FilterPart? $StamperPart?` | `requires ./metaborg.yaml by hash` | Declare that the current task depends on the provided [path](../types#path) | [unit](../types#unit) |
| [generates](#generates) | `generates $Exp $StamperPart?` | `generates file by hash` | Declare that the current task generates on the provided [path](../types#path) | [unit](../types#unit) |
| [list](#list) | `list $Exp $FilterPart?` | `list ./examples with extension "pie"` | Lists the direct children of the given [directory](../types#path). Note: for list literals, see further down this table. | A [list](../types#lists) of [paths](../types#path), i.e. `path*` |
| [walk](#walk) | `walk $Exp $FilterPart?` | `walk ./examples with extension "pie"` | Recursively get all descendants of the given [directory](../types#path) | A [list](../types#lists) of [paths](../types#path), i.e. `path*` |
| [exists](#exists) | `exists $Exp` | `exists ./config.json` | Check if a [file](../types#path) exists | [bool](../types#bool) |
| [read](#read) | `read $Exp` | `read ./config.json` | Returns the [file](../types#path) contents as a string, or null if the file does not exist | A [nullable](../types#nullable-types) [string](../types#string), i.e. `string?` |
| [return](#return) | `return $Exp` | `return false` | Returns the provided value from the current function | [unit](../types#unit). Note: may get changed to [bottom type](../types#bottom) |
| [fail](#fail) | `fail $Exp` | `fail "input cannot be null"` | Throws an ExecException with the provided [string](../types#string) as message | [unit](../types#unit). Note: may get changed to [bottom type](../types#bottom) |
| [Unit literal](#unit-literal) | `unit` | `unit` | Literal expression of the only value of the [unit type](../types#unit) | [unit](../types#unit) |
| [true](#true) | `true` | `true` | Literal expression for the [boolean](../types#bool) value `true`. | [bool](../types#bool) |
| [false](#false) | `false` | `false` | Literal expression for the [boolean](../types#bool) value `false`. | [bool](../types#bool) |
| [int literal](#int-literal) | `"-"? [0-9]+` | `0`, `23`, `-4` | A literal value of the [int type](../types#int) | [int](../types#int) |
| [null](#null) | `null` | `null` | Literal expression for the null value of [nullable types](../types#nullable-types). | [null type](../types#null-type) |
| [Tuple literal](#tuple-literal) | `($Exps)` | `(1, "one", "une")` | A literal value of a [tuple type](../types#tuples) | A [tuple type](../types#tuples) of the types of the elements |
| [List literal](#list-literal) | `[$Exps]` | `(1, 2, 3)` | A literal value of a [list type](../types#lists). For the keyword `list`, see earlier in this table. | A [list](../types#lists) of the least upper bound of the types of the elements |
| [String literal](#string-literal) | `"$StrParts"` | `"Hello $name!"` | A literal value of the [string type](../types#string) | [string](../types#string) |
| [Path literal](#path-literal) | `$PathStart$PathParts` | `./src/test/resources` | A literal value of the [path type](../types#path) | [path](../types#path) |


There is also a section on [common lexical elements](#common-lexical-elements).
This covers [filters](#filter-and-filterpart) and [stampers](#stamper-stamperpart-and-stamperkind).


## Block

Blocks are expressed as `{$Exps}`, where `$Exps` is a list of semi-colon separated expressions.
Its type and value are those of the final expressions in the block.
The final expression does not end with a semi-colon.
For example:
```
{
  val name = read ./example/name.txt;
  val greeting = read ./example/greeting.txt;
  "$greeting $name"
}
```

Empty blocks (blocks without any expression) are allowed, their type and value is [`unit`](../types#unit).

Blocks introduce their own scope.
Expressions in the block are evaluated in that scope.
Values declared in the block are not allowed to shadow values or parameters outside the block.
This means that it is not allowed to declare a value with a name that already exists.
Values declared before the block are still visible inside the block.
Values declared inside the block are not visible after the block.


## Make nullable

Make nullable is expressed as a question mark after an expression.
As its name suggests, it makes a non-nullable expression nullable.
The value remains unchanged, but the type of the expression is now [nullable](../types#nullability).
Its syntax is `$Exp?`, for example `read ./name.txt == "Bob"?`.

It is an error to use this expression on an expression that was nullable already.


## Make non-nullable

Make non-nullable is expressed as an exclamation mark after an expression.
As its name suggests, it makes a nullable expression non-nullable.
The value remains unchanged, but the type of the expression is now [non-nullable](../types#nullability).
Its syntax is `$Exp!`, for example `read file!`.

It is an error to use this expression on an expression that was non-nullable already.


## Not

Logical negation.
It takes a [boolean](../types#bool) expression and returns the opposite boolean value.
Its syntax is `!$Exp`, for example `if (!exists file) fail "$file should exist`.


## Compare for (in)equality

Compare two expressions for equality or inequality.
Two values are considered equal if they are both `null` or if the `equals` method in the backing Java class for the first value returns `true` when applied to the second value.
Otherwise, they are considered in-equal.
The syntax for equals is `$Exp == $Exp`, for example `x == null`.
The syntax for in-equals is `$Exp != $Exp`, for example `x != null`.

Expressions can only be compared if one is a non-strict subtype of the other.
This provides protection against accidentally comparing two expressions that can never be equal.

??? hint "Comparing `null` and empty lists"
    Expressions with nullable types can have equal values despite not being subtypes of each other, if they are both `null`.
    The same goes for list types with the empty list `[]`.
    In these cases, check for these specific values: `x == null && y == null`.


## Logical or

Logical or.
Takes two boolean expressions and returns `true` if either of them is `true` and `false` if both are `false`.
This operator short-circuits if the first expression is `true`, in which case the second expression will not be evaluated.
Its syntax is `$Exp || $Exp`, for example `exists file || default != null`.


## logical and

Logical and.
Takes two boolean expressions and returns `true` if both of them are `true` and `false` if either of them is `false`.
This operator short-circuits if the first expression is `false`, in which case the second expression will not be evaluated.
Its syntax is `$Exp && $Exp`, for example `configFile != null && exists configFile`.


## Addition

The add operator is an overloaded in the PIE DSL.
Its syntax is `$Exp + $Exp`.

The type of adding two values depends on their static types.
Adding two [`int`s](../types#int) uses mathematical plus: `1 + 2 // result: 3`, and the result is an `int` as well.

Adding any value to a [`string`](../types#string) converts the value to a `string` and then concatenates the strings, resulting in a `string`: `"The value is:"  + x`.
??? tip "String interpolation"
    It might be clearer to use [string interpolation.](#string)

Adding a `string` or a `path` to a relative `path` concatenates the values and results in a new `path`: `projectDir + ./src/test/resources/`
Adding a `string` or a `path` to an absolute path results in a runtime error.
??? tip "Path interpolation"
    It might be clearer to use [path interpolation.](#path)

Finally, adding a type `T2` to a list with type `T1*` has two cases

- If `T2` is a list as well both lists will be concatenated.
  The element type of `T2` must be a subtype of `T1`.

??? tip "Adding a list as an element"
    To add a list `list: T*` as an element to a list of lists `lists: T**`, wrap the list in another list: `lists + [list]`
??? info "Empty lists"
    The PIE DSL keeps track of empty lists statically.
    This allows it to give a warning when concatenating an empty list: `[1, 2, 3] + []` will give a warning.
- All other cases will append the second item to the first list.
  `T2` must be a (non-strict) subtype of `T1`.
  The element type of the resulting list is `T1`, unless `T2` is [the null type](../types#null-type).
  In that case, the element type of the resulting list is nullable as well.


## Value declaration

Value declarations declare one or more named values.
Expressions that are evaluated afterwards in the same scope or an inner scope can use the declared values by [referencing them](#value-reference).
For more information on values, see [parameters and values](../functions#parameters-and-values).

A basic value declaration declares a name with a value: `val x = 9`.
It is possible to give a type hint with the name: `val y: int? = 8`.
When a type hint is given, the type of the expression must be assignable to the type of the type hint.
The type of the declared value is the provided type from the type hint, or the type of the expression if there is no type hint.
A value declaration can also do tuple destructuring and assign its values to multiple variables at once: `val (name: string, times: int*) = getPerformance(id)`.
Each name in a tuple destructuring can have a type hint.
Tuple destructuring cannot be nested, so the following will not parse: `val (a, (b, c)) = (1, (2, 3))`.

??? example "Some examples of value declarations"
    ```
    val firstName = "Bob"; // simple value declaration
    val age: int = 27; // with type hint
    val size: (int, int) = (800, 400); // assign tuple to single value.
    val (width, height) = size; // tuple destructuring
    // tuple destructuring with type hints
    val (name: string, in: path, out: path) = ("expressions", ./in/expressions.pie, ./out/expressions.java);
    // tuple destructuring with mixed type hints
    val (year, values: (string, bool)*) = (2020, []);
    ```

Value declarations have the following syntax: `val $Binder = $Exp`, where the binder can be either a single binder `$Bind` or tuple binder `($Binds)`, and binds can be only a name `$VALID` or a name with a type hint `$VALID: Type`.

The type of a value declaration is the type of the variable(s) that it declares.
It uses the type hint if available and the expression type otherwise.
Single declarations have that single type, tuple declarations return a tuple of all the types that they declare.

## Value reference

Value references reference a declared value or parameter by name.
The name must be declared beforehand in the current scope or an outer scope.
The type and value of a value reference is the type and value of the referenced value.
The syntax is `$VALID`, for example:
```
func incrementInefficiently(x: int) -> int = {
    val y = 1;
    val res = x + y; // reference parameter x and value y
    res // reference value res
}
```


## if

An if expression conditionally evaluates an expression.
It takes two expressions.
The first one is the condition and is of type [boolean](../types#bool).
The second one is the body and can have any type.
Its syntax is `if ($Exp) $Exp`, for example `if (text == null) fail "Could not read $file"`.
If the condition evaluates to `true`, the body is evaluated, otherwise not.
The type of an `if` expression is [the `unit` type](../types#unit).
The condition and body are evaluated in their own scope, so value declarations in an `if` expression are not visible after the `if`.
Because an if expression is evaluated in its own scope and always returns the same value, the only use for an `if` expression is if the body has side-effects.

## if-else

Conditionally evaluates one of two expressions.
It takes three expressions.
The first one is the condition and is of type [boolean](../types#bool).
The second one is the true-branch and can have any type.
The third one is the false-branch and can also have any type.
Its syntax is `if ($Exp) $Exp else $Exp`, for example `if (name != null) name else default`.
If the condition evaluates to `true`, the true-branch is evaluated, otherwise the false-branch is evaluated.
The type of an if-else expression is the least upper bound of both branches.
The condition and branches are evaluated in their own scope, so value declarations in an if-else expression are not visible after the expression.

??? example "Some examples of the least upper bound of different types"
    ```
    val cat1: Cat = getCat(1);
    val cat2: Cat = getCat(2);
    val mammal: Mammal = getMammal();
    val animal: Animal = getAnimal();
    val dog: Dog = getDog();
    val fish: Fish = getFish();
    val animal1: Animal = getAnimal(1);
    val animal2: Animal = getAnimal(2);
    val catBox1: Box<Cat> = box(cat1);
    val catBox2: Box<Cat> = box(cat2);
    val anyBox1: Box<_> = box(animal1);
    val anyBox2: Box<_> = box(catBox2);

    // same type
    if (flag) "hello" else "world"  // type: string
    if (flag) 0 else 10             // type: int
    if (flag) cat1 else cat2        // type: Cat
    if (flag) animal1 else animal2  // type: Animal
    if (flag) catBox1 else catBox2  // type: Box<Cat>
    if (flag) anyBox1 else anyBox2  // type: Box<_>
    
    // subtypes
    if (flag) cat else mammal       // type: Mammal
    if (flag) catBox else anyBox    // type: Box<_>
    

    // different types
    if (flag) cat1 else dog         // type: Mammal
    if (flag) dog else cat2         // type: Mammal
    if (flag) cat2 else fish        // type: Animal
    if (flag) "hello" else 2        // type: top type
    ```


## List comprehension

List comprehensions apply an expression to every element of a list and return a new list with the new elements.
They are special syntax for mapping a list, which would not ordinarily be possible in the PIE DSL because there are no higher-order functions.
They have the syntax `[$Exp | $Binder <- $Exp]`, for example `["Key: $key; value: $value" | (key, value) <- pairs]`
The last expression is the input list and must have type `T*` for some `T`.
The binder defines names for the elements.
It can either be a single binder to bind the complete element, or a tuple binder if the element is a tuple, see [value declarations for more explanation](#value-declaration)
The first expression can use the names defined by the binder.
The type of that expression is some type `Q`.
The type of the full list comprehension is a list of the type that was mapped to, i.e. `Q*`.

??? info "Empty lists"
    A list comprehension over an empty list simply returns a new empty list.
    A list comprehension will give a warning if the input list is statically known to be empty.
    List comprehensions over empty lists are compiled to an immediate empty list of the declared type because it is not known what the element type of the empty list is.


## Function calls

Function calls [invoke a declared function](../functions#function-invocations).
They have the syntax `$ModuleList$FUNCID$TypeArgs($Exps)`, for example `stdLib:okResult<string>("Hello world!")`.
The second element is the [function name](../functions#name).
This function name can either be qualified or left unqualified by the module list.
If it is unqualified, the function name must be defined in the current module or be imported with a [function import](../modules#function-imports).
If it is qualified, [the function is looked up in that module](../modules#qualified-calls).
The number of type arguments must match the number of [type parameters on the function declaration](../functions#type-parameters), and the type arguments must be within bounds for the type parameters.
The expressions are the arguments to the function.
They must match the number of parameters that the function declared and they must be subtypes of the parameters.

The type of a call is the type of the declared function, where type parameters are replaced with their corresponding type arguments.

??? example "Return type is a generic parameter"
    ```PIE
    func id<T>(param: T) -> T = param
    func test() -> unit = {
        id<string>("Hello world!"); // type is string
        id<int>(42);                // type is int
        unit
    }
    ```

??? note "Arguments can declare values"
    [Value declarations](#value-declaration) in the arguments are legal and are visible after the call.
    Doing this is bad practice in almost all cases.
    Declare the value before the call instead.
    For example:
    ```
    // declares the value `x` with value 9
    // also passes 9 as argument to `test`
    test(val x = 9);
    x // x is visible after the call.
    ```
    Better way:
    ```
    val x = 9; // declare before call
    test(x); // refer to declared value
    x
    ```

## Method calls

Method calls [invoke](../functions#function-invocations) a [declared method](../types#methods-and-overriding).
They have the syntax `$Exp.$FUNCID$TypeArgs($Exps)`, for example `file.replaceExtension("pp.pie")`.
The first element is an arbitrary expression.
The second element is the method name.
This method is looked up on the type of the first expression.
The number of type arguments must match the number of [type parameters on the method declaration](../functions#type-parameters), and the type arguments must be within bounds for the type parameters.
The expressions are the arguments to the method.
They must match the number of parameters that the method declared and they must be subtypes of the parameters.

The type of a method call is the type of the declared method, where type parameters are replaced with their corresponding type arguments.

??? note "No methods on nullable types"
    There are no methods defined on [nullable types](../types#nullable-types).
    To access the methods of the inner type, [cast the expression to non-nullable](#make-non-nullable) first:
    ```
    val maybe: Result<string, _ : Exception> = null;
    maybe.unwrap(); // error: Cannot call method on nullable type
    maybe!.unwrap(); // type checks, but will throw a run time exception
    
    // Better: handle null value before casting
    if (maybe == null) {
        // handle null value here
        "Cannot get value, result is null"
    } else {
        maybe!.unwrap()
    }
    ```

??? example "Return type is a generic parameter"
    ```PIE
    data Box<T> = foreign java org.example.methodCall.Box {
        func get() -> T
    }
    func test(box1: Box<int>, box2: Box<bool>) -> unit = {
        box1.get(); // type is int
        box2.get(); // type is bool
        unit
    }
    ```

??? note "Expression and arguments can declare values"
    [Value declarations](#value-declaration) in the expression or the arguments are legal and are visible after the call.
    Declarations in the expression are also visible to the expressions.
    Doing this is bad practice in almost all cases.
    Declare the value before the call instead.
    For example:
    ```
    // declares the value `name` and `msg`
    // also passes 9 as argument to `test`
    // Note: getName returns an stdLib:Result<string, _ : Exception>
    (val name = getName()).unwrapOrDefault(
      // `name` is visible inside the arguments
      val msg = "Could not get name, exception: ${if (val ok = name.isOk())
          "No error"
        else
          name.unwrapErr()
        }"
    );
    (name, ok, msg); // `name`, `ok` and `message` are visible after the call.
    ```
    Better way:
    ```
    val name = getName();
    val ok = name.isOk();
    val msg = if (ok)
      "Could not get name, exception: No error"
    else
      "Could not get name, exception: ${name.unwrapErr()}"
    ```


## create supplier

[A supplier](../types#supplier) for a value can be created with the `supplier` keyword.
It has the syntax `supplier$TypeArgs($Exps)`, for example `supplier(47)` or `supplier<string>("Hello world!")`.
The type arguments can either be omitted or must be a single type argument.
The expressions are the arguments for the supplier.
There should be only one argument, the value that the supplier will supply.
The type `T` for the supplier is the type argument if it was provided, or the type of the argument otherwise.
In case a type argument is provided, the argument should be a subtype of that type argument.
The type of a supplier creation expression is `supplier<T>`.

??? note "Supplier can be treated as a normal function"
    Creating a supplier is like a normal [function call](#function calls), but built into the language grammar for implementation reasons.
    This is the only function call where the type argument is derived at the moment.


## task supplier

A task supplier expression creates a [supplier](../types#supplier) from a function.
A task supplier expression does not execute the task yet, but instead defers it until the supplier's `get` method is called.
It has the syntax `$ModuleList$FUNCID.supplier$TypeArgs($Exps)`, for example `lang:java:parse.supplier(file)`.
The second element is the [function name](../functions#name).
This function name can either be qualified or left unqualified by the module list.
If it is unqualified, the function name must be defined in the current module or be imported with a [function import](../modules#function-imports).
If it is qualified, [the function is looked up in that module](../modules#qualified-calls).
The number of type arguments must match the number of [type parameters on the function declaration](../functions#type-parameters), and the type arguments must be within bounds for the type parameters.
The expressions are the arguments to the function.
They must match the number of parameters that the function declared and they must be subtypes of the parameters.

The type of a task supplier expression is `supplier<T>`, where `T` is the type of the declared function with the type parameters replaced with their corresponding type arguments.

## requires

A requires expression expresses that the current task depends on the given [path](../types#path).
It has the syntax `requires $Exp $FilterPart? $StamperPart?`, for example `requires ./metaborg.yaml by hash` or `requires sampleDir with extension "sdf3"`.
The expression is the path to depend on.
The filter part is optional and adds a filter to filter out any paths that do not match the filter.
It is described in [the section on common lexical elements](#filter-and-filterpart).
The stamper part is also optional and provides a way to determine if a file or path is up-to-date.
It is also described in [the section on common lexical elements](#stamper-stamperpart-and-stamperkind).

The type and value of the expression is [unit](../types#unit).

!!! todo "Exceptions?"
    What happens if there is another task that provides the path? Does it quietly schedule that task before this one, does it throw an error? What if that other task runs after this task?


## generates

Marks the given [path](../types#path) as provided by the current task.
It has the syntax `generates $Exp $StamperPart?`, for example `generates file by hash`.
The expression is the path to depend on.
The stamper part is optional and provides a way to determine if a file or path is up-to-date.
It is described in [the section on common lexical elements](#stamper-stamperpart-and-stamperkind).

The type and value of this expression is [unit](../types#unit).

!!! attention "Make file modifications before using this expression"
    The contents or metadata of the file at the time that this expression is called may be cached and used for incrementality.
    Make all modifications to the file before using this expression.

!!! todo "Exceptions?"
    Can this mark a directory as provided or only a file?
    What happens when two tasks generate a file?
    What happens when this task declares it generates a file after another task has already used it?
    Can a task both require and provide a file?
    What happens if this task calls a task that provides a file and then this task also declares it generated that file?


## list

!!! info inline end "Defining list literals"
    This section is about listing children of a directory with the `list` keyword.
    To define a literal list value, see [list literal](#list-literal).

Lists direct children of the given directory.
List expressions have the syntax `list $Exp $FilterPart?`, for example `list getProjectRootDir() + ./examples with extension "pie"`.
The expression must have type [path](../types#path) and refer to an existing directory.
The filter part is optional and adds a filter to filter out any paths that do not match the filter.
It is described in [the section on common lexical elements](#filter-and-filterpart).

A list expression returns a [list](../types#lists) of the direct children of the given directory, and its type is `path*`.

!!! tip "Declaring a dependency on the directory"
    You will likely need to declare a dependency on the directory using [requires](#requires).
    You may also need to declare dependencies on the individual files if you do not call a task which already does that.

??? note "Recursive listing"
    List only gets the direct children of the given directory.
    To recursively get all files and directories in a given directory, use [walk](#walk).

!!! todo
    What happens if the starting directory does not exist?
    What happens if it is not a directory?


## walk

Recursively gets descendants of the given directory.
Walk expressions have the syntax `walk $Exp $FilterPart?`, for example `walk getProjectRootDir() + ./src/test/java with extension "java"`.
The expression must have type [path](../types#path) and refer to an existing directory.
The filter part is optional and adds a filter to filter out any files that do not match the filter.
It is described in [the section on common lexical elements](#filter-and-filterpart).

A walk expression returns a [list](../types#list) of all the files in the given directory and its descendants, and its type is `path*`.

!!! tip "Declaring a dependency on the directory"
    You will likely need to declare a dependency on the directory and all subdirectories using [requires](#requires).
    You may also need to declare dependencies on the individual files if you do not call a task which already does that.

??? note "Getting only the direct descendants"
    Walk recursively gets all files in the given directory.
    To only get direct and directories in a given directory, use [list](#list).

!!! todo
    What happens if the starting directory does not exist?
    What happens if it is not a directory?
    Does the filter also filter directories or only files?
    Should recursive directories automatically be declared [required](#require)?


## exists

Checks if a file or folder exists.
The syntax is `exists $Exp`, for example `exists ./config.json`.
The expression is the [path](../types#path) for which it should be checked if it exists.
It returns a [boolean](../types#bool) indicating whether the file or path exists.


## read

Reads the contents of the given file into a [string](../types#string).
The syntax is `read $Exp`, for example `read pie.sdf3`.
The expression is the file to be read, with type [path](../types#path).
The file is read with the system default file encoding.
It returns a string with the contents of the file.


## Return

Returns from the current function with the provided value.
Its syntax is `return $Exp`, for example `return true` or `return errResult<FileNotFoundException>(createFileNotFoundException("could not find $file"))`.
The expression is evaluated and its value returned.
The type of the expression should be a subtype of the declared [return type of the current function](../functions#return-type).

The type of a return expression is [unit](../types#unit).

??? attention "Type may get changed to bottom type"
    The type of a return expression may be changed to [the bottom type](../types#bottom) in the future.
    This would allow using a return expression as a branch in an if-else expression.


## fail

Throws an `ExecException` with the provided `string` as message.
This exits the function, any code after this expression is not evaluated.
Its syntax is `fail $Exp`, for example `fail "Could not open $file, it does not exist"`
The expression is the message for the exception and must be of type [string](../types#string).

The type of a fail expression is [unit](../types#unit).

??? attention "Type may get changed to bottom type"
    The type of a fail expression may be changed to [the bottom type](../types#bottom) in the future.
    This would allow using a fail expression as a branch in an if-else expression.

??? tip "consider using `Result<T, E>`"
    Fail throws an exception, which cannot be handled in the PIE DSL.
    We recommend using `Result<T, E>` from the PIE standard library instead.


## Unit literal

`unit` is a literal expression of the only value of the [unit type](../types#unit).


## True

`true` is the literal expression for one of the two values of the [boolean type](../types#boolean).

## False

`false` is the literal expression for one of the two values of the [boolean type](../types#boolean).


## int literal

Int literals are a literal value of the [int type](../types#int).
Their syntax is `"-"? [0-9]+`, for example `0`, `1`, `2`, `-1`, `47` and `-30774`.
That is an optional dash (unary minus, `-`), followed by some digits.
This syntax is lexical, meaning that there cannot be any layout between the sign or digits.

???+ attention "valid int values"
    Int literals represent literal values of the int type.
    As such, they must be valid values of the int type, i.e. in the range $-2^{31}$ to $2^{31}-1$, inclusive.
    This is currently not enforced, and breaking this constraint will lead to Java compile errors after compiling the PIE code.

    `-0` is allowed and equal to `0`.

??? example "Examples"
    ```
    // Valid integer literals:
    0
    1
    234
    2349273
    -4
    -237894
    -0 // same as 0
    0010 // same as 10

    // invalid integer literals
    - 12 // not allowed to have a space between the minus and the digits. Unary minus is not supported.
    1 024 // spaces between digits are not allowed
    2,048 // commas between digits are not allowed
    324.346 // periods between digits are not allowed. Floats do not exist in PIE, separators are not supported.
    DEADBEEF // letters are not allowed
    0b0101011110010 // binary notation is not supported
    0x234e9617ab7 // hexadecimal notation is not supported
    abd547 // this is not a hexadecimal value  but a value reference
    ten // this is not an int literal but a value reference
    ```


## null

`null` is the value that is added by making a type [nullable](../types#nullable-types).
It is also a value of the [top type](../types#top).


## Tuple literal

Tuple literals express literal values of the [tuple type](../types#tuples).
Their syntax is `($Exps)`, for example `("scala", "VF_SCALA", walk (subjectScalaSrcDir + ./lib/scala.jar))`.
The expressions are the elements of the tuple.
There must be at least two elements.
The type of a tuple literal is the tuple type of the types of the elements, so the literal `(1?, "a string", true)` has type `(int?, string, bool)`.

??? note "Tuples with less than two elements"
    It is not possible to express tuples with zero or a single element.
    Zero element tuples cannot be expressed by design.
    Their common use case as a [unit type](../types#unit) is covered by the [unit literal](#unit-literal) instead.
    Single element tuples will be parsed as a [bracketed expression](#expressions) instead.

??? tip "Tuple literals from subtype elements"
    Tuple types cannot be assigned to each other in most cases, so the following is not possible:
    ```
    data Fruit = $DataImpl
    data Apple : Fruit = $DataImpl
    data Pear : Fruit = $DataImpl

    func getApple() -> Apple = $FuncImpl
    func getPear() -> Pear = $FuncImpl

    // type (Apple, Pear) cannot be assigned to (Fruit, Fruit)
    func example() -> (Fruit, Fruit) = (getApple(), getPear())
    ```
    
    To create such a tuple, assign the elements explicitly to the correct types first:
    ```
    func example() -> (Fruit, Fruit) = {
        val apple: Fruit = getApple();
        val pear: Fruit = getPear();
        (apple, pear)
    }
    ```


## List literal

!!! info inline end "List keyword"
    This section is about defining list literals.
    For information on the `list` keyword, see [list expressions](#list), which list the children of a directory.

Define a literal [list](../types#lists) value.
The syntax is `[$Exps]`, for example `[1, 2, 3]`, or `[apple, banana, pear]`.
The expressions are the elements of the list.
The least upper bound of the types of the expressions is the list element type `T`.
The type of the list literal is a list of `T`, i.e. `T*`.
The list element type must not be the top type.

??? attention "Empty list literals may lead to Java errors"
    The empty list literal `[]` has a special type for implementation reasons.
    It compiles to a list with the [bottom type](../types#bottom).
    As such, the generated Java code may have compile errors.


## String literal

Define a literal value of type [string](../types#string).
The syntax is `"$StrParts"`, where `$StrParts` are parts of the string.
String parts are lexical, which means that there cannot be any layout between them (layout between string parts will be part of the string).
The possible string parts are:


- A sequence of characters excluding `$`, `"`, `\` and newlines, for example `A sequence of characters = 123!?`.
This expresses that exact sequence of characters.
- `$` followed by the name of a value or parameter, for example `$dir`.
This converts the value to a string.
It is an error to use an undefined name.
- `${$Exp}`, for example `${1 + 2}`.
This evaluates the expression and converts the resulting value into a string.
- `\$`.
This represents the literal character `$`.
- `\` followed by another character.
This represents a character according to [Java semantics](https://docs.oracle.com/javase/specs/jls/se8/html/jls-3.html#jls-3.10.6).
For example, `\n` is a newline character, `\\` is a single backslash, and `\r` is a carriage return character.
In particular, `\"` represents the literal character `"`, and does not end the string literal.

All of the string parts are concatenated into a single string value without separating characters between them.


## path literal

Define a literal value of type [path](../types#path).
The syntax is `$PathStart$PathParts`, for example `/home/alice/very-important-documents` or `./src/test/resources/`.
`$PathStart` is either `/` for absolute paths or `./` for relative paths.`$PathParts` are parts of the path.
Path start and path parts are lexical, which means that there cannot be any layout between them (layout between path parts will result in parse errors).
The possible path parts are:


- A sequence of characters excluding `$`, `"`, `\` and layout, for example `path/to/the/goods`.
This expresses that exact sequence of characters.
- `$` followed by the name of a value or parameter, for example `$rootDir`.
The value must be of type path.
It is an error to use an undefined name.
- `${$Exp}`, for example `${getProjectDir()}`.
This evaluates the expression.
The resulting value must be of type path.
- `\$`.
This represents the literal character `$`.
- `\` followed by another character.
This represents a character according to [Java semantics](https://docs.oracle.com/javase/specs/jls/se8/html/jls-3.html#jls-3.10.6).
For example, `\\` is a single backslash.

The path start and all of the path parts are concatenated into a single path value without separating characters between them.

??? note "Path validity and existence (is not checked)"
    The validity or existence of path literals is not checked.
    This means that a path literal like `.////.` is allowed, even though it would be invalid for most file systems.
    To check if a path exists, use [exists](#exists).


## Common lexical elements

This section describes common lexical elements that are used by multiple expressions.


### Filter and FilterPart

Filters are used expressions that read directories from the filesystem, so [requires](#requires), [list](#list) and [walk](#walk).
They are used to keep certain paths and ignore all other paths based on the name and the extension.
They have the syntax `with $Filter`, for example `with extension "str"` or `with patterns ["test-res", "result", "generated"]`
The possible filters are listed in the table below.

| name | expression | description |
| --- | --- | --- |
| Regex | `regex $Exp` | Keeps files if they match the provided regular expression. The expression must be a [string](../types#string) representing a regular expression. Todo: Figure out what exactly it matches on (full path, name, includes extension?), regex flavor (Java, some other kind?) |
| Pattern | `pattern $Exp` | Keeps files if the name contains the provided string. The expression must be a [string](../types#string). TODO: I assume that this only needs to match part of the name and does not include the extension |
| Patterns | `patterns $Exp` | Keeps files if the name contains any of the provided strings. The expression must be a [list](../types#list) of [strings](../types#string). TODO: I assume that this only needs to match part of the name and does not include the extension |
| Extension | `extension $Exp` | Keeps files if the file extension matches the provided string. The extension must match the string exactly, so `pie` is different from `PIE` and `PIE-simple`. The string should not include the period (`.`) separating the filename and the file extension. The expression must be a [string](../types#string). TODO: I assume that it needs to be an exact match. Can it match `pp.pie`? |
| Extensions | `extensions $Exp` | Keeps files if the file extension matches any of the provided strings. The extension must match one of the strings exactly, so `pie` is different from `PIE` and `PIE-simple`. The strings should not include the period (`.`) separating the filename and the file extension. The expression must be a [list](../types#list) of [strings](../types#string). TODO: I assume that it needs to be an exact match. Can it match `pp.pie`? |

!!! todo
    Find exact semantics for the filters.
    Can they handle directories or do they only work on files?
    See also todos in the table.

??? note "Multiple filters"
    It is not allowed to use multiple filters.
    If you need multiple filters, encode your requirements in a regex filter instead.


### Stamper, StamperPart and StamperKind

A Stamper specifies how it is determined whether a path is up-to-date when executing incrementally.
They are used by [requires](#requires) and [generates](#generates).
They use the syntax `by $StamperKind`, where the stamper kind can be `hash` or `modified`.

Stamping `by hash` will calculate the md5 hash of a file and assume that the file is up to date if the hash matches the cached hash.
Stamping `by modified` will check the modification time, and assumes it is up-to-date when that time is at or before the cached time.

??? note "Checking the full file contents"
    There is currently no way in the PIE DSL to specify that the full file contents should match for a file to be considered up-to-date.
    If you need this, write the task in Java or use [`read file`](#read).

!!! todo
    Does it work for directories or only files?
    Does the hash calculate md5 hash or another hash?
    What happens when a file is generated `by modified` but required `by hash`?
    What is the default modifier?
