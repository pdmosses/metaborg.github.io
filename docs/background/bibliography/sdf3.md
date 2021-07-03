# An SDF3 Bibliography

SDF3[@AmorimV20] is the third generation in the SDF family of syntax definition formalisms, which were developed in the context of the ASF+SDF [5], Stratego/XT [10], and Spoofax [38] language workbenches.

## SDF

The first SDF [23] supported modular composition of syntax definition,
a direct correspondence between concrete and abstract syntax, and parsing
with the full class of context-free grammars enabled by the Generalized-LR
(GLR) parsing algorithm [44,56]. Its programming environment, as part of the
ASF+SDF MetaEnvironment [40], focused on live development of syntax definitions through incremental and modular scanner and parser generation [24–26]
in order to provide fast turnaround times during language development.

## SDF2

The second generation, SDF2 encompassed a redesign of the internals of
SDF without changing the surface syntax. The front-end of the implementation
consisted of a transformation pipeline from the rich surface syntax to a minimal
core (kernel) language [58] that served as input for parser generation. The key
change of SDF2 was its integration of lexical and context-free syntax, supported
by Scannerless GLR (SGLR) parsing [60,61], enabling composition of languages
with different lexical syntax [12].

## SDF3

SDF3 is the latest member of the family and inherits many features of its
predecessors.
The most recognizable change is to the syntax of productions that
should make it more familiar to users of other grammar formalisms.
Further, it introduces new features in order to support multi-purpose interpretations of syntax definitions.
The goals of the design of SDF3 are (1) to support the definition of the concrete and abstract syntax of formal languages (with an emphasis on programming languages), (2) to support declarative syntax definition so that there is no need to understand parsing algorithms in order to understand definitions [39], (3) to make syntax definitions readable and understandable so that they can be used as reference documentation, and (4) to support execution of syntax definitions as parsers, but also for other syntactic operations, i.e to support multi-purpose interpretation based on a single source.
The focus on multipurpose interpretation is driven by the role of SDF3 in the Spoofax language workbench [38].



## References

\bibliography
