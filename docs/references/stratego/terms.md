# Terms

Stratego programs transform terms. When using Stratego for program
transformation, terms typically represent the abstract syntax tree of a
program. But Stratego does not much care what a term represents. Terms
can just as well represent structured documents, software models, or
anything else that can be rendered in a structured format.

Generally program text is transformed into a term by means of parsing,
and turned back into program text by means of pretty-printing. One way
to achieve this is by using
[[SDF3]{.doc}](../../sdf3/index.html){.reference .internal}. For most of
the examples, we will just assume that we have terms that should be
transformed and ignore parsing and pretty-printing. However, when we
turn to running examples in the Spoofax environment in the Eclipse IDE,
we will rely on SDF3 as that is the primary way to produce terms in
Spoofax/Eclipse.

## Annotated Term Format

Terms in Stratego are terms in the *Annotated Term Format*, or *ATerms*
for short. The ATerm format provides a set of constructs for
representing trees, comparable to XML or abstract data types in
functional programming languages. For example, the code
`4 + f(5 * x)` might be represented in
a term as:

```
Plus(Int("4"), Call("f", [Mul(Int("5"), Var("x"))]))
```

ATerms are constructed from the following elements:

-   **Integer**: An integer constant, that is a list of decimal digits,
    is an ATerm.

    Examples: `1`, `12343`{.docutils
    .literal .notranslate}.

-   **String**: A string constant, that is a list of characters between
    double quotes is an ATerm. Special characters such as double quotes
    and newlines should be escaped using a backslash. The backslash
    character itself should be escaped as well.

    Examples: `"foobar"`,
    `"string with quotes\""`,
    `"escaped escape character\\ and a newline\n"`.

-   **Constructor application**: A constructor is an identifier, that is
    an alphanumeric string starting with a letter, or a double quoted
    string.

    A constructor application `c(t1,...,tn)` creates a term by applying a constructor to a list of
    zero or more terms. For example, the term
    `Plus(Int("4"),Var("x"))`uses the
    constructors `Plus`,
    `Int`, and `Var` to create a nested term from the strings
    `"4"` and `"x"`.

-   **List**: A list is a term of the form `[t1,...,tn]`, that is a list of zero or more terms between
    square brackets. While all applications of a specific constructor
    typically have the same number of subterms, lists can have a
    variable number of subterms. The elements of a list are typically of
    the same type, while the subterms of a constructor application can
    vary in type.

    Example: The second argument of the call to `"f"` in the term `Call("f",[Int("5"),Var("x")])` is a list of expressions.

-   **Tuple**: A tuple `(t1,...,tn)` is
    a constructor application without a constructor.

    Example: `(Var("x"), Type("int"))`

-   **Annotation**: The elements defined above are used to create the
    structural part of terms. Optionally, a term can be annotated with a
    list of terms. These annotations typically carry additional semantic
    information about the term. An annotated term has the form
    `t{t1,...,tn}`.

    Example: `Lt(Var("n"),Int("1")){Type("bool")}`. The contents of annotations is up to the application.

## Persistent Representation

The term format described above is used in Stratego programs to denote
terms, but is also used to exchange terms between programs. Thus, the
internal format and the external format exactly coincide. Of course,
internally a Stratego program uses a data-structure in memory with
pointers rather than manipulating a textual representation of terms. But
this is completely hidden from the Stratego programmer.

## Namespaces

qualified names ... 

!!! todo
