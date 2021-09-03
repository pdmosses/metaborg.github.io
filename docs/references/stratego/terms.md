# Terms

Stratego programs transform terms.

For example, the code `4 + f(5 * x)` might be represented in a term as:

```aterm
Plus(Int("4"), Call("f", [Mul(Int("5"), Var("x"))]))
```

## Term Forms

Terms are constructed from the following forms.


### Integer

```stratego
$Digit+
```

An integer constant, that is a list of decimal digits, is an ATerm.

Examples: `1`, `12343`.


### String

```stratego
"$Char*"
```

A string constant, that is a list of characters between double quotes is an ATerm.
Special characters such as double quotes and newlines should be escaped using a backslash.
The backslash character itself should be escaped as well.

Examples: `"foobar"`, `"string with quotes\""`, `"escaped escape character\\ and a newline\n"`.


### String Templates

```stratego
$[$TemplateChar*]
```

Multiline strings can be _constructed_ using string templates.

```stratego
$[if [code1] then
   [code2]]
```

The indentation will be computed relative to the start of the template.

String templates can also include _escapes_ to term expressions producing strings or integers.

For example, the string above includes escapes to include `code1` and `code2` and the following error message

```stratego
$[error: variable [x] is not defined]
```

includes the name of the variable `x`.


### Constructor application

```stratego
$Constructor($Term,...,$Term)
```

A constructor is an identifier, that is an alphanumeric string starting with a letter, or a double quoted string.

A constructor application `c(t1,...,tn)` creates a term by applying a constructor to a sequence of zero or more terms.

For example, the term `Plus(Int("4"),Var("x"))`uses the constructors `Plus`, `Int`, and `Var` to create a nested term from the strings `"4"` and `"x"`.

The parentheses are needed even when a constructor has no subterms, in order to avoid ambiguity with [variables](#term-patterns).
Thus, `True()` is a constructor application, but `True` is a variable.


### List

```stratego
[$Term, ..., $Term]
```

A list is a term of the form `[t1,...,tn]`, that is a list of zero or more terms between square brackets.
While all applications of a specific constructor typically have the same number of subterms, lists can have a variable number of subterms.
The elements of a list are typically of the same type, while the subterms of a constructor application can vary in type.

Example: The second argument of the call to `"f"` in the term `Call("f",[Int("5"),Var("x")])` is a list of expressions.


### Tuple

```stratego
($Term, ..., $Term)
```

A tuple `(t1,...,tn)` is a constructor application without a constructor.

Example: `(Var("x"), Type("int"))`


### Annotation

```stratego
$PreTerm{$Term, ..., $Term}
```

Any of the term forms above can be annotated with a list of terms.  

Example: `Lt(Var("n"),Int("1")){Type("bool")}`.

Only 'preterms', i.e. terms without annotations, can be annotated.
The form `Var("a"){Type("bool")}{Value(3)}` is syntactically incorrect.


## Term Patterns

A term _pattern_, is a term extended with _variables_.

In the term pattern

```stratego
Plus(e, Int("0"))
```

the identifier `e` is a variable that stands for any term.


### Linear vs Non-Linear

A pattern is _linear_ if each variable occurs at most once, _non-linear_ otherwise.
The _non-linear_ pattern

```stratego
Plus(e, e)
```

stands for a `Plus` term with identical arguments.

A term pattern without variables (aka term) is _ground_.


### Substitution

_Substitution_ is the process of applying a map from variables to terms to a term pattern, replacing occurrence of variables in the domain of the map with the corresponding terms in the co-domain of the map.

_Substitution_ is also the name for the mapping of variables to terms.


### Pattern Matching

_Pattern matching_ is the process of matching a ground term against a term pattern.

A term `t` matches a term pattern `p` iff there is a substitution `S` such that applying the substitution to the pattern `S(p)` yields the term `t`.


## Persistent Representation

The term format described above is used in Stratego programs to denote
terms, but is also used to exchange terms between programs.
Thus, the internal format and the external format exactly coincide.
Of course, internally a Stratego program uses a data-structure in memory with
pointers rather than manipulating a textual representation of terms.
But this is completely hidden from the Stratego programmer.

!!! todo
    API for reading, writing terms?


## Namespaces

Currently, the constructors of terms live in a global namespace.
In the future, we want to support qualified names.


## References

Terms in Stratego are inspired by terms in the *Annotated Term Format*, or *ATerms* for short[@BrandJKO00].
The ATerm format provides a set of constructs for representing trees, comparable to XML or abstract data types in functional programming languages.

\bibliography
