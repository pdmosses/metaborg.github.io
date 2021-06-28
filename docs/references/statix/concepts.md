# Language Concepts

In this section, a brief description of the main concepts of the Statix language
is provided.

## Terms

The data model that underlies all Statix specifications is algebraic data.
Besides several built-in primitives, such as integer and string literals, users
can build composite terms using term constructors, tuples and lists. Statix is
a sorted logic, in the sense that all runtime data should adhere to a
multi-sorted signature.

## Constraints

Key to the Statix design philosophy is to view a type-checking problem as a
constraint problem. When solving the constraint problem, a minimal model is inferred
from the constraints. This model represents a principal typing for the original
program. In order to express such constraint problems, a versatile set of built-in
constraints is provided by the Statix language. For more information on constraints,
see the [Basic Constraints](../basic-constraints) section.

## Rules

Besides using built-in constraints, users can define their own constraints using
constraint handling rules. Rules consist of a head and a body. The head specifies
the arguments to the constraint, and (optionally) a guard, which indicates when
to apply the rule. The body is a regular constraint, which, when proven, asserts
that the constraint holds. More detailed information about user-defined constraints
can be found in the [Rules](../rules) section.

## Scope Graphs

Since Statix is especially designed for type-checking, and type-checking is heavily
intertwined with name binding, special support for name binding is integrated
in the language. Name binding is modelled using _scope graphs_, in which _scopes_
are represented as nodes, visibility is modelled using _labelled edges_ between
nodes, and _declarations_ using special terminal nodes that are associated with
a particular datum. References are modelled using _scope graph queries_. For
more information on scope graph construction and querying, see sections
[Scope Graph Constraints](../scope-graphs) and [Queries](../queries), respectively.
