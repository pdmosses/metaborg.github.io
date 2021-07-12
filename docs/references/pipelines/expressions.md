# Expressions

Function bodies in PIE DSL consist entirely of expressions.
Every expression has a type and returns a value of that type, with the exception of `fail` and `return`.

Expressions can use brackets to override the default priority rules, for example `a && (b || c)`.
Brackets have the following form: `($Exp)`

This section describes expressions in the PIE DSL.
Expressions can use declared values.
These are described [in this section of the functions documentation](../functions#parameters-and-values).

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

Empty blocks (blocks without any expression) are allowed, their type and value is [`unit`](../types#unit).

Blocks introduce a their own scope.
Expressions in the block are evaluated in that scope.
Values declared in the block are not allowed to shadow values or parameters outside the block.
This means that it is not allowed to declare a value with a name that already exists.
Values declared before the block are still visible inside the block.


# ToNullable



# ToNonNullable
# Not

# equal
# not equal
# or
# and

# addition


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
# String literal
# path literal
