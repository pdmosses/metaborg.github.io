# Spoofax Development
This is the reference manual for building and developing Spoofax, as well as information about its internals.

## Introduction
Spoofax is the integration of many different tools, compilers, (meta-)languages, (meta-)libraries, and runtime components. This integration is made concrete in the [spoofax-releng](https://github.com/metaborg/spoofax-releng) Git repository on GitHub. This repository contains all components via [Git submodules](https://git-scm.com/book/en/v2/Git-Tools-Submodules), which are updated by our [build farm](https://buildfarm.metaborg.org/view/Spoofax/job/metaborg/job/spoofax-releng/) that builds Spoofax whenever one of its components in a submodule changes.

Spoofax currently contains the following subcomponents as submodules:

- [`releng`](https://github.com/metaborg/spoofax-deploy/) - Release engineering scripts for managing and building the spoofax-releng repostory.
- Java libraries and runtimes
    - [`mb-rep`](https://github.com/metaborg/mb-rep/) — Libraries for program representation such as abstract terms
    - [`mb-exec`](https://github.com/metaborg/mb-exec/) — Stratego interpreter and utilities
    - [`jsglr`](https://github.com/metaborg/jsglr/) — JSGLR parser
    - [`spoofax`](https://github.com/metaborg/spoofax/) — Spoofax Core, a cross platform API to Spoofax languages
    - [`spoofax-maven`](https://github.com/metaborg/spoofax-maven/) — Maven integration for Spoofax Core
    - [`spoofax-sunshine`](https://github.com/metaborg/spoofax-sunshine/) — Command-line integration for Spoofax Core
    - [`spoofax-eclipse`](https://github.com/metaborg/spoofax-eclipse/) — Eclipse plugin for Spoofax Core
    - [`spoofax-intellij`](https://github.com/metaborg/spoofax-intellij/) — IntelliJ plugin for Spoofax Core
- Meta-languages and libraries
    - [`esv`](https://github.com/metaborg/esv/) — Editor service language
    - [`sdf`](https://github.com/metaborg/sdf/) — Syntax Definition Formalisms, containing the SDF2 and SDF 3 languages
    - [`stratego`](https://github.com/metaborg/stratego/) and [`strategoxt`](https://github.com/metaborg/strategoxt/) — Stratego compiler, runtime, and editor
    - [`nabl`](https://github.com/metaborg/nabl/) — Name binding languages, containing the NaBL and NaBL2 languages, and support libraries for NaBL2
    - [`ts`](https://github.com/metaborg/ts/) — Type system language
    - [`dynsem`](https://github.com/metaborg/dynsem/) — Dynamic semantics language
    - [`metaborg-coq`](https://github.com/metaborg/metaborg-coq/) — Coq signatures and syntax definition
    - [`spt`](https://github.com/metaborg/spt/) — Spoofax testing language
    - [`runtime-libraries`](https://github.com/metaborg/runtime-libraries/) — NaBL support libraries, incremental task engine for incremental name and type analysis

Furthermore, this repository contains a Bash script `./b` that redirects into the Python release engineering scripts in the `releng` submodule. These scripts support managing this Git repository, version management, generation of Eclipse instances, building Spoofax, and releasing new versions of Spoofax.

The following how-tos explain how to set up Maven and other required tools for building and developing Spoofax, how to build and develop Spoofax, how to write this documentation, and explains some of the internals of Spoofax components.

- [Requirements](requirements.md)
- [Maven](maven.md)
- [Building](building.md)
- [Developing](developing.md)
- [Releasing](releasing.md)
