# How to Generate a Stratego Signature

It is tedious to write a signature that is in sync with a syntax definition.
Therefore, Spoofax automatically generates a signature from a syntax definition for the abstract syntax trees that the parser for that syntax definition produces.


## Write a Syntax Definition

In the `/syntax/` directory in your language project for language `lang` write a syntax definition in file `lang.sdf3`.

Possibly write additional syntax defininitions modules and import the in `lang.sdf3`.

Example.
Consider the following SDF3 syntax definition:

```sdf3
module lang
imports Base

lexical sorts IntConst
lexical syntax
  IntConst = [0-9]+
sorts Exp
context-free syntax
  Exp.Int     = IntConst  
  Exp.Plus    = [[Exp] + [Exp]]   {left}
  Exp.Minus   = [[Exp] - [Exp]]   {left}
  Exp         = [([Exp])] {bracket}
context-free priorities
  {left : Exp.Plus Exp.Minus}
```


## Generate Signature

The build for your language project will invoke the SDF3 compiler to generate a signature file for each SDF3 file in your project in directory `/src-gen/signatures/` with suffix `-sig` and extension `.str`.

The build should be invoked as soon as you save a file.

Thus `lang.sdf3` generates `/src-gen/signatures/lang-sig.str`.

Example.
For the SDF3 file above, the following signature is automatically generated:

```stratego
module signatures/lang-sig
imports signatures/Base-sig

signature
  sorts IntConst
  sorts Exp
  constructors
                   : string -> IntConst
    Int            : IntConst -> Exp
    Plus           : Exp * Exp -> Exp
    Minus          : Exp * Exp -> Exp
    IntConst-Plhdr : IntConst
    Exp-Plhdr      : Exp
    IntConst-Plhdr : COMPLETION-INSERTION -> IntConst
    Exp-Plhdr      : COMPLETION-INSERTION -> Exp
```

The injection from strings into the lexical `IntConst` sort reflects the fact that tokens are represented as strings in ASTs.
The placeholder constructors generated for the sorts are used to represent incomplete programs and syntactic code completion[@AmorimEWV16].


## Use Signature

To use the signature, import it into the Stratego module that uses its constructors.

Example.
To use the signature for the example import it as follows:

```stratego
module desugar
imports signatures/lang-sig
rules
  // ...
```


## References

\bibliography
