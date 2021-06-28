# Types


## Signatures

To use terms in Stratego programs, their constructors should be declared
in a signature. A signature declares a number of sorts and a number of
constructors for these sorts. For each constructor, a signature declares
the number and types of its arguments. For example, the following
signature declares some typical constructors for constructing abstract
syntax trees of expressions in a programming language:

```
    signature
      sorts Id Exp
      constructors
               : String -> Id
        Var    : Id -> Exp
        Int    : Int -> Exp
        Plus   : Exp * Exp -> Exp
        Mul    : Exp * Exp -> Exp
        Call   : Id  * List(Exp) -> Exp
```

Currently, the Stratego compiler only checks the arity of constructor
applications against the signature. Still, it is considered good style
to also declare the types of constructors in a sensible manner for the
purpose of documentation.

The situation in Spoofax/Eclipse is even more convenient; if you have an
SDF3 language specification, Spoofax will automatically generate a
corresponding signature definition that you can import into Stratego.


## Transformation Types
