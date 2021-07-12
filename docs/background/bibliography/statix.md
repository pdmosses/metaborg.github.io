# A Statix Bibliography

The Statix[@AntwerpenPRV18] [@RouvoetAPKV20] meta-language provides support for the declarative definition of the static semantics of programming languages in terms of unification constraints and scope graph constraints for name resolution[@AntwerpenPRV18] guaranteeing query stability[@RouvoetAPKV20].
Here we trace the development of the Statix language.

## The NaBL Name Binding Language

The NaBL[@KonatKWV12] language provides support for the declaration of the name binding rules of programming languages in terms of _definitions_, _references_, and _scoping_.

The NaBL _task engine_ supports incremental execution of type checkers based on NaBL[@WachsmuthKVGV13].

While the paper used the WebDSL language as example, the NaBL analysis was only applied in production in the SDF3 language.

The NaBL language is very declarative, but binding patterns such as sequential let and 'subsequent scope' are difficult to express in it.

## Scope Graphs

The study of the semantics of NaBL (and its limits in expressiveness) led to the formulation of a general theory of name resolution based on scope graphs[@NeronTVW15].

The vertices of scope graphs are scopes and the edges model reachability.
Declarations are associated with scopes.
Name resolution by means of a declarative resolution calculus is defined as finding a path from the scope of a reference to the scope of a declaration taking into account the structure of the scope graph extended with visibility rules formulated in terms of path well-formedness and path specificity.

## Constraint Language

Based on the theory of name resolution, a constraint language was defined with a declarative and operational semantics[@AntwerpenNTVW16].

The language was designed for a two stage type checking process.
In the first phase unification and scope constraints are generated, in the second phase these constraints are solved.
A distinctive feature of this approach with respect to other constraint-based approaches to type checking, is the fact that name resolution is deferred until constraint resolution.
This makes the definition of type-dependent name resolution, e.g. for computing the types of record fields, straightforward.

The NaBL2 language was a concrete implementation of this design and was integrated into Spoofax.
It featured concrete syntax for unification and scope graph constraints, and rules for mapping AST nodes to constraints.

The two stage type checking process entailed limitations for the type systems that could be expressed in NaBL2.
In particular, it was not possible to generate constraints based on information computed during the second stage.
For example, a subtyping rule operating on types computed during constraint resolution

Furthermore, the NaBL2 language itself was untyped, making it easy to make errors in specifications.

## Statix Language

The Statix language[@AntwerpenPRV18] was designed to overcome the limitations of NaBL2.

The language is typed, with signatures describing the types of ASTs, and typing rules declaring the types of predicates.
The type system of Statix is expressed in NaBL2, making the specification of rules statically checked and much less prone to errors.
This also provided a useful testbed of the ideas of scope graphs and constraints.

The generation and resolution of constraints is intertwined, in order to allow computing constraints over inferred information.

Furthermore, in order to generalize the notions of visibility supported by the NaBL2 language, Statix features query constraints, in order to relate references to declarations, but also to compute sets of names based on broader criteria.
For example, the definition of structural record types can be expressed by a query that produces all fields of a record.

Necessarily these changes entail that queries need to be executed in a scope graph that is not in its final form.

This necessitate a theory of query stability.
Name resolution queries such be scheduled such that they produce stable results, i.e. results that would also be produced at the end of the process.
The this end a theory of _critical edges_ was developed that asserts when it is safe to perform a query in a certain scope[@RouvoetAPKV20].

The Statix solver implements the operational semantics on the language in order to automatically derive type checkers from specifications.
Optimizations of this solver can be based on the generaly underlying theory and be applied to all languages for which Statix specifications have been written.
One such optimization is the derivation of _implicitly parallel_ type checkers from Statix specifications[@AntwerpenV21-preprint].

## Editor Services

A next step in the evolution of Statix is the derivation of semantic editor services such as renaming and code completion from specifications[@PelsmaekerAV19].

## References

\bibliography
