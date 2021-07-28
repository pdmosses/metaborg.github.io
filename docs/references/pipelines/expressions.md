# Expressions

Function bodies in PIE DSL consist entirely of expressions.
Every expression has a type and returns a value of that type, with the exception of `fail` and `return`.

Expressions can use brackets to override the default priority rules, for example `a && (b || c)`.
Brackets have the following form: `($Exp)`

This section describes expressions in the PIE DSL.
Expressions can use declared values.
These are described [in this section of the functions documentation](../functions#parameters-and-values).

!!! todo
    Give overview of priorities

!!! todo
    Add overview table: name, syntax, example, description, type





# Block

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


# Make nullable

Make nullable is expressed as a question mark after an expression.
As its name suggests, it makes a non-nullable expression nullable.
The value remains unchanged, but the type of the expression is now [nullable](../types#nullability).
Its syntax is `$Exp?`, for example `read ./name.txt == "Bob"?`.

It is an error to use this expression on an expression that was nullable already.


# Make non-nullable

Make non-nullable is expressed as an exclamation mark after an expression.
As its name suggests, it makes a nullable expression non-nullable.
The value remains unchanged, but the type of the expression is now [non-nullable](../types#nullability).
Its syntax is `$Exp!`, for example `read file!`.

It is an error to use this expression on an expression that was non-nullable already.


# Not

Logical negation.
It takes a [boolean](../types#bool) expression and returns the opposite boolean value.
Its syntax is `!$Exp`, for example `if (!exists file) fail "$file should exist`.


# Compare for (in)equality

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


# Logical or

Logical or.
Takes two boolean expressions and returns `true` if either of them is `true` and `false` if both are `false`.
This operator short-circuits if the first expression is `true`, in which case the second expression will not be evaluated.
Its syntax is `$Exp || $Exp`, for example `exists file || default != null`.


# logical and

Logical and.
Takes two boolean expressions and returns `true` if both of them are `true` and `false` if either of them is `false`.
This operator short-circuits if the first expression is `false`, in which case the second expression will not be evaluated.
Its syntax is `$Exp && $Exp`, for example `configFile != null && exists configFile`.


# Addition

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


# Value declaration

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
The value of a value declaration is simply the value of the expression.

# Value reference

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


# if

An if expression conditionally evaluates an expression.
It takes two expressions.
The first one is the condition and is of type [boolean](../types#bool).
The second one is the body and can have any type.
Its syntax is `if ($Exp) $Exp`, for example `if (text == null) fail "Could not read $file"`.
If the condition evaluates to `true`, the body is evaluated, otherwise not.
The type of an `if` expression is [the `unit` type](../types#unit).
The condition and body are evaluated in their own scope, so value declarations in an `if` expression are not visible after the `if`.
Because an if expression is evaluated in its own scope and always returns the same value, the only use for an `if` expression is if the body has side-effects.

# if-else

Conditionally evaluates one of two expressions.
It takes three expressions.
The first one is the condition and is of type [boolean](../types#bool).
The second one is the true-branch and can have any type.
The third one is the false-branch and can also have any type.
Its syntax is `if ($Exp) $Exp else $Exp`, for example `if (name != null) name else default`.
If the condition evaluates to `true`, the true-branch is evaluated, otherwise the false-branch is evaluated.
The type of an if-else expression is the least upper bound of both branches.
It is an error if the least upper bound of the two branches is [the top type](../types#top).
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
    if (flag) "hello" else 2        // type: top type, error
    ```


# ListComprehension

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


# Function calls

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

# Method calls

Method calls [invoke](../functions#function-invocations) a [declared method](../types#methods-and-overriding).
They have the syntax `$Exp.$FUNCID$TypeArgs($Exps)`, for example `file.replaceExtension("pp.pie")`.
The first element is an arbitrary expression.
The second element is the method name.
This method is looked up on the type of the first expression.
The number of type arguments must match the number of [type parameters on the method declaration](../functions#type-parameters), and the type arguments must be within bounds for the type parameters.
The expressions are the arguments to the method.
They must match the number of parameters that the method declared and they must be subtypes of the parameters.

The type of a method call is the type of the declared method, where type parameters are replaced with their corresponding type arguments.

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


# create supplier

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


# task supplier

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

# requires

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


# generates

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


# list

Lists direct children of the given directory.
To define a literal list value, see [list literal](#list-literal).
List expressions have the syntax `list $Exp $FilterPart?`, for example `list getProjectRootDir() + ./examples with extension "pie"`.
The expression must have type [path](../types#path) and refer to an existing directory.
The filter part is optional and adds a filter to filter out any paths that do not match the filter.
It is described in [the section on common lexical elements](#filter-and-filterpart).

A list expression returns a [list](../types#list) of the direct children of the given directory, and its type is `path*`.

!!! tip "Declaring a dependency on the directory"
    You will likely need to declare a dependency on the directory using [requires](#requires).
    You may also need to declare dependencies on the individual files if you do not call a task which already does that.

??? note "Recursive listing"
    List only gets the direct children of the given directory.
    To recursively get all files and directories in a given directory, use [walk](#walk).

!!! todo
    What happens if the starting directory does not exist?
    What happens if it is not a directory?


# walk

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


# exists

Checks if a file or folder exists.
The syntax is `exists $Exp`, for example `exists ./config.json`.
The expression is the [path](../types#path) for which it should be checked if it exists.
It returns a [boolean](../types#bool) indicating whether the file or path exists.


# read

Reads the contents of the given file into a [string](../types#string).
The syntax is `read $Exp`, for example `read pie.sdf3`.
The expression is the file to be read, with type [path](../types#path).
The file is read with the system default file encoding.
It returns a string with the contents of the file.


# Return

Returns from the current function with the provided value.
Its syntax is `return $Exp`, for example `return true` or `return errResult<FileNotFoundException>(createFileNotFoundException("could not find $file"))`.
The expression is evaluated and its value returned.
The type of the expression should be a subtype of the declared [return type of the current function](../functions#return-type).

The type of a return expression is [unit](../types#unit).

??? attention "Type may get changed to bottom type"
    The type of a return expression may be changed to [the bottom type](../types#bottom) in the future.
    This would allow using a return expression as a branch in an if-else expression.


# fail

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


# Unit literal
# True
# False
# int literal
# null
# Tuple literal
# List literal

Define a literal list value.
To list the children of a directory, see [list expressions](#list).


# String
# path literal

# Common lexical elements

This section describes common lexical elements that are used by multiple expressions.


## Filter and FilterPart

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


## Stamper, StamperPart and StamperKind

A Stamper specifies how it is determined whether a path is up-to-date when executing incrementally.
They are used by [requires](#requires) and [generates](#generates).
They use the syntax `by $StamperKind`, where the stamper kind can be `hash` or `modified`.

Stamping `by hash` will calculate the md5 hash of a file and assume that the file is up to date if the hash matches the cached hash.
Stamping `by modified` will check the modification time, and assumes it is up-to-date when that time is after the cached time.

??? note "Checking the full file contents"
    There is currently no way in the PIE DSL to specify that the full file contents should match for a file to be considered up-to-date.
    If you need this, write the task in Java or use [`read file`](#read).

!!! todo
    Does it work for directories or only files?
    Does the hash calculate md5 hash or another hash?
    What happens when a file is generated `by modified` but required `by hash`?
    What is the default modifier?
