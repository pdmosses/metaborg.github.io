# Concrete Syntax

When writing language-to-language transformations in Stratego, it is possible to use different approaches, for example, writing AST-to-AST transformations. However, to write such transformations, the language engineer needs to know the constructors of both languages. Moreover, AST nodes in rules that define such transformations may contain many nested children, making the work of writing such rules cumbersome and error-prone. Note that Stratego only statically checks the name and arity of constructors, thus, errors would only be detected when pretty-printing the generated AST to the target language.

As an example of this approach, the rule below specifies a transformation of a Calc program to a Java program.

```stratego
program-to-java :
  Program(stats) -> CompilationUnit(None()
                                      , []
                                    , [ ClassDeclaration(
                                          [Public()]
                                        , Id("Program")
                                        , None()
                                        , None()
                                        , None()
                                        , [ MethodDecl(
                                              [Public(), Static()]
                                            , MethodHeader(
                                                java-type
                                              , Id("eval")
                                              , NoParams()
                                              , []
                                              , None()
                                              )
                                            , Block(
                                                [ java-stats*
                                                ]
                                              )
                                            )
                                          ]
                                        )
                                      ]
                                    )
  with
      java-type   := ...
      java-stats* := ...
```

An alternative approach consists of using string interpolation. Instead of generating abstract terms of the target language, transformations generate source code directly, interpolating strings with boilerplate code of the target language and variables defined in the transformation itself. The problem with this approach is that syntax errors in the string fragments of the target language are not detected statically.

Consider the rule shown previously, rewritten below using string interpolation (the code between $[ and ]). Note that if the fragment would contain a typo, the syntax error would only be detected after the code had been generated. Note also that one can interpolate Stratego variables with the fragment of the target language by escaping them between [ and ].

```stratego
program-to-java :
  Program(stats) -> $[public class Program {
                        public static [java-type] eval() {
                          [java-stats]
                        }
                      }
                     ]
  with
      java-type   := ...
      java-stats  := ...
```

The third option is to use concrete syntax. When using concrete syntax, the transformation is still AST-to-AST but the AST of the target language is abstracted over using the concrete syntax of the language instead. That is, the concrete syntax fragment is parsed internally producing an AST, and that AST is resulted from the transformation.

The same rule defined using concrete syntax is shown below. Note that any syntax error in the fragment would in fact, be detected by the editor, as the fragment is being parsed internally. Moreover, the fragment also has the syntax highlighting of the target language when shown by the editor.

```stratego
program-to-java :
  Program(stats) -> compilation-unit
                      |[ public class Program {
                           public static ~type:java-type eval() {
                             ~bstm*:java-stats*
                           }
                         }
                      ]|
  with
    java-type   := ...
    java-stats* := ...
```

There are two aspects to consider when enabling concrete syntax inside Spoofax. The first one is being able to write Stratego transformations with fragments of a target (or source) language. In other words, the first aspect consists of generating a mixed parse table that embeds the desired target language inside Stratego. The second aspect consists of including the parse table inside an Spoofax project, adding an additional .meta file to then enable concrete syntax for a specific Stratego file. Below, we describe both aspects with more detail.

## Mixing Grammars 

To generate a mixed parse table that embeds a language inside Stratego, it is necessary to modify the original Stratego grammar, extending it with the desired language. One problem that may occur when combining the grammars of two different languages is name clashing, i.e., non-terminals that have the same name in Stratego and the embedded language. For that reason, the embedding occurs using a modified Stratego grammar, which renames all Stratego context-free non-terminals using by prefixing it with `StrategoLang`, avoiding name clashes. Inside Spoofax, you can add a source dependency on the `org.metaborg:stratego.lang:${metaborgVersion}` project in you `metaborg.yaml` file, then you can import the so-called namespaced grammar.

Once you have access to the namespaced grammar, the next step consists of defining the embedding grammar, the grammar that actually mixes the two languages. A grammar that embeds one language into another may contain three types of productions: productions that define quotations for elements of the target language in the host language, productions that define anti-quotations back to the host language from the target language, and variables, which are shortcuts to anti-quotations, and may appear inside the target language fragments.

When embedding a language into Stratego, it is common to allow fragments of the host language as Stratego terms. For that reason, quotation productions are injected into Stratego terms. For example, the productions below, written in SDF3, indicates that a Java compilation unit can occur in Stratego in a place where a Stratego term can occur.

```{.sdf3 .no-ligatures}
imports
  StrategoLang/sugar/terms-namespaced
  java/packages/CompilationUnits

context-free syntax
  StrategoLang-PreTerm.ToTerm = <compilation-unit |[ <CompilationUnit> ]|>
  StrategoLang-PreTerm.ToTerm = <|[ <CompilationUnit> ]|>
```

Anti-quotation productions define points to insert elements of the host language inside fragments of the target language. For example, with the production below, we allow Stratego terms to occur in a Java fragment whenever a non-terminal `Type` can occur.

```{.sdf3 .no-ligatures}
imports
  java/types/Main

context-free syntax
  Type.FromTerm = [~[StrategoLang-Term]]
  Type.FromTerm = [~type:[StrategoLang-Term]]
```

Note that the constructor `FromTerm` indicates that productions represent anti-quotations. Furthermore, note that anti-quotations may also be named after the non-terminal being referenced (e.g., `~type:`).

Using anti-quotations might make the fragment of the target language quite verbose. Therefore, it is also possible to define variables as shortcuts to anti-quotations. For example, the productions below define variables to reference anti-quotations to `Type` fragments. That is, instead of reference to a Stratego variable `X` by using `~type:X`, one may name this variable `t_1` which corresponds to a variable for a non-terminal `Type`.

```sdf3
variables
  Type = "t_" [0-9\']* {prefer}
```

The `prefer` annotation indicates that in case of an ambiguity, the variable production should be preferred.

Using the three types of productions above, it is possible to specify which fragments one wants to write using concrete syntax and which symbols may appear inside these fragments as Stratego variables (using anti-quotation or variables with a specific name).

Finally, it is necessary to define a module `Stratego-<LanguageName>` that should import the Stratego grammar and the embedding grammar. This module should be defined in a file named `Stratego-<LanguageName>.sdf3` and put in the `syntax` folder so that Spoofax can locate it and build the mixed table. That is, if we define the module for our `Stratego-Java` mixed grammar:

```sdf3
module Stratego-Java

imports
  EmbeddedJava
  StrategoLang/import-namespaced

context-free start-symbols
  StrategoLang-Module
```

Note that it is necessary to define the start symbol of the mixed grammar as `StrategoLang-Module`. After defining the embedding grammar and the `Stratego-<LanguageName>` module, Spoofax generates the mixed table inside the trans folder when rebuilding the project.


## Using Mixed Parse Tables to Allow Concrete Syntax

Assuming a mixed parse table has been successfully generated or already exists, the next step is to allow concrete syntax in transformations using that table. The table needs to be in a folder that can be discovered by the Stratego compiler. By default it will be generated in the `trans` folder of the project that defines the mixed grammar, to be used within the project. If you wish to use the mixed grammar in another project, make sure to export the generate table by adding an entry for it in the `metaborg.yaml` file. Then any other project that depends on your mixed grammar project with a source dependency will also provide the table file to the Stratego compiler.

Next, together with the file in which we would like to enable concrete syntax, it is necessary to create a `.meta` file with the same name. That is, to enable concrete syntax in a file `generate.str`, it is necessary to create, in the same directory, an addition file `generate.meta`. This file should indicate which mixed table should be used to parse `generate.str`. For that reason it should contain:

```aterm
Meta([Syntax("<ParseTableName>")])
```

where `<ParseTableName>` is the filename of the parse table without extension, `Stratego-Java` in our example.

With the configuration above, Spoofax automatically detects that the file contains concrete syntax and use that table to parse it. In that file, one may write rules containing concrete syntax as defined by the productions in the mixed grammar.
