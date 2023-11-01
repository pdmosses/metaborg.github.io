# An SDF3 Bibliography

SDF3[@AmorimV20] is the third generation in the SDF family of syntax definition formalisms, which were developed in the context of the ASF+SDF[@BrandDHJ01], Stratego/XT[@BravenboerKVV08], and Spoofax[@KatsV10] language workbenches.

Kats et al. decribe the motivation for declarative syntax definition[@KatsVW10].

## SDF

The first SDF[@HeeringHKR89] supported modular composition of syntax definition,
a direct correspondence between concrete and abstract syntax, and parsing
with the full class of context-free grammars enabled by the Generalized-LR
(GLR) parsing algorithm[@Tomita85] [@Rekers1992].
Its programming environment, as part of the ASF+SDF MetaEnvironment[@Klint93], focused on live development of syntax definitions through incremental and modular scanner and parser generation[@HeeringKR92] [@HeeringKR90] [@HeeringKR94]
in order to provide fast turnaround times during language development.

## SDF2

The second generation, SDF2 encompassed a redesign of the internals of
SDF without changing the surface syntax.
The front-end of the implementation consisted of a transformation pipeline from the rich surface syntax to a minimal core (kernel) language[@Visser95] that served as input for parser generation.
The key change of SDF2 was its integration of lexical and context-free syntax, supported by Scannerless GLR (SGLR) parsing[@Visser97] [@Visser97-SGLR], enabling composition of languages with different lexical syntax[@Visser02] [@BravenboerV04].

## SDF3

SDF3 is the latest member of the family and inherits many features of its
predecessors.
The most recognizable change is to the syntax of productions that
should make it more familiar to users of other grammar formalisms.
Further, it introduces new features in order to support multi-purpose interpretations of syntax definitions.
The goals of the design of SDF3 are (1) to support the definition of the concrete and abstract syntax of formal languages (with an emphasis on programming languages), (2) to support declarative syntax definition so that there is no need to understand parsing algorithms in order to understand definitions [@KatsVW10], (3) to make syntax definitions readable and understandable so that they can be used as reference documentation, and (4) to support execution of syntax definitions as parsers, but also for other syntactic operations, i.e to support multi-purpose interpretation based on a single source.
The focus on multipurpose interpretation is driven by the role of SDF3 in the Spoofax language workbench [@KatsV10].

Key features of SDF3 include

- Template productions[@VollebregtKV12]
- Error recovery[@JongeKVS12]
- Layout constraints for layout-sensitive syntax[@ErdwegRKO12] [@AmorimSEV18]
- Safe and complete disambiguation of expression grammars[@Amorim2019]
- Placeholders and syntactic code completion[@AmorimEWV16]

## Future Work

Parse table composition[@BravenboerV08], while implemented in a prototype, hasn't made into the production implementation yet.



## References

\bibliography
