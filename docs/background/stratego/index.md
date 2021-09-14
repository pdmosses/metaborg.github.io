# Stratego

The Stratego transformation was born from a pure rewriting approach to program transformation by the introduction of _traversal combinators_[@LuttikV97] and _programmable rewriting strategies_[@VisserBT98].

## Strategic Rewriting

This section reviews the classic definition of term rewriting and motivates the transition to strategic rewriting.

- [Term rewriting](strategic-rewriting/term-rewriting.md)
- [Limitations of term rewriting](strategic-rewriting/limitations-of-rewriting.md)
- [Factoring out Traversal](strategic-rewriting/traversal-with-rules.md)
- [Strategic Rewriting](strategic-rewriting/strategic-rewriting.md)

## Strategy Combinators

Rather than defining high-level strategies as primitives, Stratego provides basic strategies combinators for composing strategies.
The [section](../../references/stratego/strategy-combinators.md) in the reference manual provides a definition of all the combinators.
Here we expand that description with many examples.

- [Sequential combinators](strategy-combinators/sequential.md)
- [Term combinators](strategy-combinators/term.md)
- [Traveral combinators](strategy-combinators/traversal.md)
- [Type unifying traversals](strategy-combinators/type-unifying.md)

## Origin Tracking

Origin tracking is a term rewriting feature that has been put into Stratego to track connections between terms through a transformation. If you for example parse a file into an abstract syntax tree (AST) and the parser leaves some information about what term refers to what part of the file, you can keep track of that even after transformations.

However, origin tracking in Stratego is rather limited, and people are often confused about how it works. On [the page for Origin Tracking](origin-tracking.md) you can find an explanation of origin tracking, how it works in Stratego, and plans on future improvements. 

## References

\bibliography
