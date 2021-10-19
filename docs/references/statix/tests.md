# Tests

Statix has its own test format. These tests can help to debug your specification
and isolate issues. In this section, we explain the format and the output of
such tests.

## Test Format

Statix tests should reside in `*.stxtest` files, and look as follows:

```statix
resolve $Constraint

$Section*
```

At the top level, the `#!statix resolve` keyword indicates this is a test file.
After this keyword, the constraint that should be solved when executing the test
is provided. Finally, any section that can be found in a regular [module](modules.md)
can be added to a test.

A test can be executed using the traditional or the concurrent solver with the
`Spoofax > Evaluate > Evaluate Test` or `Spoofax > Evaluate > Evaluate Test
(Concurrent)` menu, respectively.

## Test Output

When a test is executed, a `.stxresult` file with the test result will open. This
file contains three sections.

First, under the `substitution` header, a mapping from the top-level existentially
quantified variables to their values is provided. Due to the normalization Statix
applies, there are sometimes additional entries for wildcards and return values
of functional predicates.

Secondly, under `analysis` and `scope graph`, the scope graph that models the
test constraint is shown. A scope graph consists of a list of scope terms, which
look as follows

```statix
$ScopeName {
  relations {
    $RelationID : $Term+
  }
  edges {
    $LabelID: $Scope+
  }
}
```

That is, for each label and relation for which entries exists in a scope, a list
of associated scopes/data is shown.

!!! note "Empty Scopes"
    Note that no entry for an empty scope will be present.

Finally, under the `errors`, `warnings` and `notes` headers, the appropriate
messages of these types are shown. The message value is equal to the top line
of a regular Statix message, but no traces are displayed. Terms in templates are
formatted three levels deep.
