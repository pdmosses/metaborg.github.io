# Strategy Combinators

Rather than building in rewrite rules and high-level strategies, Stratego provides _strategy combinators_ as basic building blocks from which these can defined

strategies [@VisserBT98]

core language [VisserB98] to which more complex strategies can be desugared

!!! warning
    While it useful to understand the constructs defined in this and the next sections, their use should be avoided in favour of the higher-level language constructs where possible.

## Identity and Failure

The most basic operations in Stratego are id and fail. The identity strategy id always succeeds and behaves as the identity function on terms. The failure strategy fail always fails. The operations have no side effects.

## Sequential Composition

The sequential composition s1 ; s2 of the strategies s1 and s2 first applies the strategy s1 to the subject term and then s2 to the result of that first application. The strategy fails if either s1 or s2 fails.

## Left Choice

## Guarded Choice

## Match

## Build

## Variable Scope


## Calling Primitives



## References

\bibliography
