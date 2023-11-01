---
title: "Code Highlighting"
description: "Applying code highlighting in documentation code blocks."
---

# Documentation Code Highlighting

## Block Highlighting
To apply code highlighting to a block of code, surround it with triple backticks (`` ``` ``) and write the name of the language after the starting backticks, like this:

=== "Markdown"
    ````
    ```python
    def foo():
        pass
    ```
    ````

=== "Output"
    ```python
    def foo():
        pass
    ```


## Inline Highlighting
To apply code highlighting to inline code, surround the code with single backticks (`` ` ``) and add `` #! `` after the initial backtick, followed by the language name:

=== "Markdown"
    ````
    Call the `#!python def foo()` function.
    ````

=== "Output"
    Call the `#!python def foo()` function.


## Languages
The highlighter supports all languages supported by [Pygments](https://pygments.org/).

The Pygments project has [a list of all supported languages](https://pygments.org/docs/lexers/). To use a language, refer to it through one of its _short names_.

Additionally, in this Spoofax documentation these [Spoofax languages](https://github.com/metaborg/metaborg-pygments) are supported:

| Short name    | Language                                         |
| ------------- | ------------------------------------------------ |
| `aterm`       | [ATerms](../../references/stratego/terms.md).    |
| `dynsem`      | DynSem.                                          |
| `esv`         | [ESV](../../references/esv/index.md).            |
| `flowspec`    | [FlowSpec](../../references/flowspec/index.md).  |
| `nabl`        | NaBL.                                            |
| `nabl2`       | NaBL2.                                           |
| `sdf3`        | [SDF3](../../references/sdf3/index.md).          |
| `statix`      | [Statix](../../references/statix/index.md).      |
| `stratego`    | [Stratego](../../references/stratego/index.md).  |
