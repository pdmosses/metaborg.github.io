# Dynamic Rules

Plain [rewrite rules](rewrite-rules.md) are context-free, i.e. do not take their context into account.
Context-sensitive transformations can be defined by passing context information using additional arguments to rules and strategies.
Alternatively, Stratego provides linguistic support to dynamically define rewrite rules based on context information[@BravenboerDOV06].


## Defining Dynamic Rules

```stratego
rules( $Id : $Rule ... )
```

A dynamic rule definition is a regular (conditional) [rewrite rule](rewrite-rules.md) that is defined as part of a strategy rather than at top-level.

The difference is that any variables that are bound in the context of the rule, take their binding from the context, rather then being universally quantified.
Thus, a dynamic rule instance can be thought of as having the context variables replaced by the corresponding terms from the context.

Example.
The following strategy `DefineInlineCall` defines the dynamic rule `InlineCall`:

```stratego
DefineInlineCall =
  ?FunDef(f, args, e)
  ; rules(
      InlineCall :
        Call(f, es) -> Let(dec*, e)
        where <zip(\(x, e) -> VarDec(x, e)\)> (args, es) => dec*
    )
```

The variables `f`, `args`, and `e` in the dynamic rule are bound in context, while the variables `es` and `dec*` are universally quantified.
The variables `x` and `e` in the embedded lambda rule are local to that rule.
Thus, the application

```stratego
<DefineInlineCall>
   FunDef("inc", ["x"], Add(Var("x"), Int("1")))
```

can be thought of to give rise to the definition

```stratego
InlineCall :
  Call("inc", es) -> Let(dec*, Add(Var("x"), Int("1")))
  where <zip(\(x, e) -> VarDec(x, e)\)> (["x"], es) => dec*
```


## Invoking Dynamic Rules

When `$Id` is defined as a dynamic rule it can be invoke like a regular rule or strategies.
The invocation only succeeds when applied to a term that coincide with the left-hand side pattern variables bindings inherited from the context.

Thus, in the example above `InlineCall` can be called to invoke a previously defined dynamic rule.
For example, the following are calls to `DefineInlineCall` and `InlineCall`

```stratego
<DefineInlineCall>
   FunDef("inc", ["x"], Add(Var("x"), Int("1")))

<InlineCall>
   Call("inc", [Mul(Var("y"), Int("3"))]) =>
   Let([VarDec("x", Mul(Var("y"), Int("3")))],
       Add(Var("x"), Int("1")))

<InlineCall>
   Call("foo", []) // fails
```

Note that the application to `Call("foo", [])` fails since it does not match the dynamically defined rule.


## Parameterized Dynamic Rules

Dynamic rules can be parameterized like regular rewrite rules and strategies.


## Multiple Definitions

Dynamic rules can be defined for multiple contexts simultaneously.

For example, the following applications of `DefineInlineCall`

```stratego
<DefineInlineCall>
   FunDef("inc", ["x"], Add(Var("x"), Int("1")))

<DefineInlineCall>
   FunDef("twice", ["y"], Mul(Var("x"), Int("2")))
```

can be thought of defining multiple top-level rewrite rules

```stratego
InlineCall :
  Call("inc", es) -> Let(dec*, Add(Var("x"), Int("1")))
  where <zip(\(x, e) -> VarDec(x, e)\)> (["x"], es) => dec*

InlineCall :
  Call("twice", es) -> Let(dec*, Mul(Var("y"), Int("2")))
  where <zip(\(x, e) -> VarDec(x, e)\)> (["y"], es) => dec*
```


## Overriding Dynamic Rules

A definition of a dynamic rule _with the same left-hand side_ as a previous definition, overrides that previous definition.

Thus, if after the applications of `DefineInlineCall` above, we apply

```stratego
<DefineInlineCall>
   FunDef("twice", ["z"], Add(Var("z"), Var("z")))
```

Then the dynamic rule for `twice` above is _undefined_, and instead the rule

```stratego
InlineCall :
  Call("twice", es) -> Let(dec*, Add(Var("z"), Var("z")))
  where <zip(\(x, e) -> VarDec(x, e)\)> (["z"], es) => dec*
```

is added to the collection of rules.


## Dynamic Rule Scope

It is possible to limit the _scope_ in which dynamic rule definitions are available.
The _dynamic rule scope_ `{| $Id ... : $Strategy |}` limits the availability of dynamic rules named `$Id ..` defined within the brackets to that scope.
After exiting the scope, the state of the dynamic rule definitions before the scope is restored.

For example, the following strategy defines inlining rules that are only available during the visit of the body of the `Let`:

```stratego
  inline :
    Let(dec1*, e1) -> Let(dec2*, e2)
    with <inline> dec1* => dec2*
    with {| InlineCall
          : <map(try(DefineInlineCall))> dec2*
          ; <inline> e1 => e2
          |}
```

Application of this strategy to the program term

```stratego
Let([FunDef("inc", [..], ..)
    , FunDef("twice", [..], ..)]
  , Add(
      Let([FunDef("twice", [..], [..])]
        , Call("twice", [..])) // inline second def of twice
      , Call("twice", [..]) // inline first def of twice
    )
)
```

will result in locally overriding the first dynamic rule for `"twice"`, but undoing that override at the end of the dynamic rule scope, such that it is available again at the second call to `"twice"`.

While dynamic rule scopes can deal with lexical scope systems, the preferred way to deal with scope in programming languages is to perform name (and type) analysis using the [Statix](../statix/index.md) meta-language and perform a uniquify transformation to guarantee unique names.


## Multiple Right-Hand Sides

In order to collect multiple ways to rewrite a term use `rules( $Id :+ $Rule)`.

For example, the following is a small API for for emitting nodes in a control-flow graph consisting of blocks.  

```stratego
add-cfg-node  :: CBlock -> CBlock
all-cfg-nodes :: List(CBlock) -> List(CBlock)

add-cfg-node =
  ?block
  ; rules( CFGNode :+ _ -> block )

all-cfg-nodes =
  <bagof-CFGNode <+ ![]>()
```

The `bagof-$Id` strategy is generated automatically and produces all right-hand sides corresponding to a left-hand side.

## Other Dynamic Rule Extensions

The papers by Olmos and Visser[@OlmosV05] and Bravenboer et. al[@BravenboerDOV06] describe more advanced features of dynamic rules, primarily inspired by data-flow transformations.
For defining data-flow analyses, Spoofax now provides the [FlowSpec](../flowspec/index.md) meta-language.



## References

\bibliography
