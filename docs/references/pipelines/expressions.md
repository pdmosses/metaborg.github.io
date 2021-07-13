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

!!! hint
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
??? tip
    It might be clearer to use [string interpolation.](#string)

Adding a `string` or a `path` to a relative `path` concatenates the values and results in a new `path`: `projectDir + ./src/test/resources/`
Adding a `string` or a `path` to an absolute path results in a runtime error.
??? tip
    It might be clearer to use [path interpolation.](#path)

Finally, adding a type `T2` to a list with type `T1*` has two cases

- If `T2` is a list as well both lists will be concatenated.
  The element type of `T2` must be a subtype of `T1`.

??? tip
    To add a list `list: T*` as an element to a list of lists `lists: T**`, wrap the list in another list: `lists + [list]`
??? info
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

??? example
    Some examples of value declarations
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
# if-else
# ListComprehension

# Function calls
// can be qualified
// type args
# Method calls

# create supplier
# task supplier

Note: getting from a supplier

# requires
# generates
// with regex, pattern, patterns, extension, extensions
// by modified, hash

# list
# walk

# exists
# read

# Return
# fail
// not recommended as it quits the entire pipeline, recommend to use Result<T, E> from the standard library

# Unit literal
# True
# False
# int literal
# null
# Tuple literal
# List literal
# String
# path literal
