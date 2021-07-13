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


# Compare for equality

Compare two expressions for equality.
Two values are considered equal if they are both `null` or if the `equals` method in the backing Java class for the first value returns `true` when applied to the second value.
Its syntax is `$Exp == $Exp`, for example `x == 0`


# Compare for inequality

Compare two expressions for inequality.
Two values are considered in-equal if exactly one of them is `null` or if the `equals` method in the backing Java class for the first value returns `false` when applied to the second value.
Its syntax is `$Exp != $Exp`, for example `x != 0`


# Logical or

Logical or.
Takes two boolean expressions and returns `true` if either of them is `true`.
This operator short-circuits if the first expression is `true`, in which case the second expression will not be evaluated.
Its syntax is `$Exp || $Exp`, for example `exists file || default != null`.


# logical and

Logical and.
Takes two boolean expressions and returns `true` if both of them are `true`.
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

// single, tuple
// type hints

# Value References


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
