# A Stratego Bibliography

The original publication on Stratego appeared in ICFP'98[@VisserBT98] and introduced named rewrite rules and a language of strategy combinators with an operational semantics.
An important aspect of the design of Stratego is the separation of the language in a core language[@VisserB98] of strategy combinators and a high-level 'sugar' language of rewrite rules that can be desugared to the core language.
This is still the way that the Stratego compiler is organized.

The original also introduced contextual terms.
These where eventually replaced by [dynamic rewrite rules](/reference/stratego/rules/dynamic-rules.md)[@BravenboerDOV06].
The paper about dynamic rules[@BravenboerDOV06] also provides a comprehensive overview of Stratego and its operational semantics.


Stratego and its ecosystem are described in a number of system description papers, including
Stratego 0.5[@Visser01],
Stratego/XT 0.16[@BravenboerKVV06],
Stratego/XT 0.17[@BravenboerKVV08]


Recently, a gradual type system was designed for Stratego[@SmitsV20].
This design and its incremental compiler[@SmitsKV20] are the basis for the Stratego2 version of the language.

## References

\bibliographystyle{plain}
\bibliography
