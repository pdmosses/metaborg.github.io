# Inspect Terms

As a Stratego programmer you will be looking a lot at raw ATerms.
Stratego pioneers did this by opening an ATerm file in *emacs* and
trying to get a sense of the structure by parenthesis highlighting and
inserting newlines here and there. These days your life is much more
pleasant through pretty-printing ATerms, which adds layout to a term to
make it readable. For example, parsing the following program

```
   let function fact(n : int) : int =
          if n < 1 then 1 else (n * fact(n - 1))
     in printint(fact(10))
    end
```

produces the following ATerm:

```
    Let([FunDecs([FunDec("fact",[FArg("n",Tp(Tid("int")))],Tp(Tid("int")),
    If(Lt(Var("n"),Int("1")),Int("1"),Seq([Times(Var("n"),Call(Var("fact"),
    [Minus(Var("n"),Int("1"))]))])))])],[Call(Var("printint"),[Call(Var(
    "fact"),[Int("10")])])])
```

By pretty-printing the term we get a much more readable term:

```
    Let(
      [ FunDecs(
          [ FunDec(
              "fact"
            , [FArg("n", Tp(Tid("int")))]
            , Tp(Tid("int"))
            , If(
                Lt(Var("n"), Int("1"))
              , Int("1")
              , Seq([ Times(Var("n"), Call(Var("fact"), [Minus(Var("n"), Int("1"))]))
                    ])
              )
            )
          ]
        )
      ]
    , [ Call(Var("printint"), [Call(Var("fact"), [Int("10")])])
      ]
    )
```


In Spoofax/Eclipse, you will find that in some contexts ATerms are
automatically pretty-printed, whereas in others they are simply printed
linearly. However, you can obtain assistance with perceiving the
structure of any ATerm by writing it into a file with the ".aterm"
extension and opening it in the Spoofax Editor in Eclipse. On the right
there will be a convenient Outline Navigator which allows you to select
any node in the ATerm and see the entire subtree below it highlighted in
the editor.
