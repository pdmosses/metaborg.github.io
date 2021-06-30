---
template: index.html
title: "Spoofax: The Language Designer's Workbench"
hide:
  - navigation
  - toc
hero:
  title: "Spoofax: The Language Designer's Workbench"
  subtitle: An open-source language designer's workbench with everything you need for designing your next textual (domain-specific) programming language.
  install_button: Getting Started
  source_button: Source Code
  nightly_link: Nightly A{{ config.extra.release.dev.version }}B
features:
  - title: Syntax
    image: /assets/syntax.png
    description: Declaratively specify your syntax and pretty-printer using the Syntax Definition Formalism 3 (SDF3) language.
  - title: Static Semantics
    image: /assets/semantics.png
    description: Use Statix to declare the type system and name binding using <em>scope graphs</em>.
  - title: Term Transformations
    image: /assets/transformation.png
    description: Write an interpreter or compiler using term transformations in Stratego.
---

# The Spoofax Language Workbench

Spoofax is a platform for developing textual (domain-specific) programming languages.
The platform provides the following ingredients:

- Meta-languages for high-level declarative language definition
- An interactive environment for developing languages using these meta-languages
- Code generators that produces parsers, type checkers, compilers, interpreters, and other tools from language definitions
- Generation of full-featured Eclipse editor plugins from language definitions
- An API for programmatically combining the components of a language implementation

With Spoofax you can focus on the essence of language definition and ignore irrelevant implementation details.

[Get started](getting-started.md) by downloading and installing Spoofax or build it [from source](https://github.com/metaborg/spoofax-releng).
