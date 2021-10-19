# Known bugs and limitations

This page lists the known bugs and limitations of the PIE DSL, and workarounds if they exist.
If you have an issue that is not listed here, please check if it is listed on our Github page, and if not, open a new issue there: https://github.com/metaborg/pie/issues.

!!! todo "Missing section: how to troubleshoot"
    <!-- Also rename this section / page? -->

## Compiler generates invalid code for void return types

The Java type `void` does not exist in the PIE DSL.
Instead, it uses `unit` to signify that the return type does not hold a useful value.
Right now, the compiler will generate incorrect code for `void` functions, which results in Java compile errors in the generated code.
There is no specific workaround for this, but [the standard workarounds for unsupported Java functions](#standard-workarounds-for-unsupported-java-functions) should work.
In the future, the compiler will support functions that are declared to have a `unit` return type but which have `void` return type.

## Standard workarounds for unsupported Java features

The PIE DSL has less features than Java by design.
This sometimes means that Java elements cannot be used as is in the PIE DSL.
This sections lists some standard workarounds for these issues.

### Standard workarounds for unsupported Java functions

This section provides workarounds for calling Java functions that are not supported by the PIE DSL.

!!! todo "Missing section: standard workarounds for unsupported Java functions"
    In summary, the workarounds are:

    1. Write a wrapper function
    2. Implement the task in Java. (Do not call the function from the PIE DSL, but call it from Java instead)

### Standard workarounds for unsupported Java data types

!!! todo "Missing section: standard workarounds for unsupported Java data types"
