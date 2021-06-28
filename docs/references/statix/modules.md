# Modules

A Statix Specification is organised as a collection of modules. Each module
corresponds to a file with a `.stx` extension.

## Module Structure

The structure of a Statix module looks as follows:

```statix
module $ModuleName

$Section*
```

Each module declares its name, and subsequently contains a number of sections.
The module name should coincide with the relative path of the module with respect
to the closest source root.

!!! check
    Link to documentation on source roots.

## Imports

In an `imports` section, definitions from other modules can be brought in scope.

```statix
imports

  $ModuleName*
```

Modules can only be imported with their fully qualified name. That is, for each
`$ModuleName` in an `imports` section, a module with exactly the same name must exist.

Imports of sorts, constructors and predicates are transitive, while imports of
labels and relations are non-transitive.

## Signatures

In a `signature` section, type definitions are located.

```statix
signature

  $Signature*
```

Examples of signatures are: sort and constructor declarations or label and relation
declarations. Each of these will be explained in the appropriate subsection.

## Rules

In a `rules` section, the rules of a specification are defined. For more
information on rules, see the [Rules](../rules) section.

```statix
rules

  $RuleDeclaration*
```
