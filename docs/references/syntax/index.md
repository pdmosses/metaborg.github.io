# SDF3

SDF3 is the meta-language in Spoofax for syntax definition.

A syntax definition is structured as a collection of [modules](modules/), which may import each other.

[Symbols](symbols/) are the building blocks of [productions](productions/).
Productions are defined for [lexical](lexical-syntax/), [context-free](context-free-syntax/), or [kernel](kernel-syntax/) syntax.

[Start symbols](start-symbols/) indicate the entry point of a syntax definition.

SDF3 automatically generates a pretty-printer for [template](templates/)-based productions.

Grammars can be [disambiguated](disambiguation/) by means of rejects, priorities, associativity, and restrictions.

SDF3 provides additional constructs for the definition of [layout-sensitivite](layout-sensitivity/) languages.

Permissive grammars are automatically generated for [error-recovery](recovery/) parsing. Handwritten recovery rules can be added to tweak recovery behavior.

## Source

The sources of the SDF3 implementation can be found at

- https://github.com/metaborg/sdf/tree/master/org.metaborg.meta.lang.template: The SDF3 language implementation (SDF3 was called TemplateLang before and it has not been renamed everywhere yet)