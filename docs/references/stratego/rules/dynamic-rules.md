# Dynamic Rules

Plain [rewrite rules](rewrite-rules.md) are context-free, i.e. do not take their context into account.
Context-sensitive transformations can be defined by passing context information using additional arguments to rules and strategies.
Alternatively, Stratego provides linguistic support to dynamically define rewrite rules based on context information[@BravenboerDOV06].


## Defining Dynamic Rules

A dynamic rule definition is a regular (conditional) [rewrite rule](rewrite-rules.md) that is defined as part of a strategy rather than at top-level.
A dynamic rule definition has the form

```stratego
rules( $Id : $Rule ... )
```

The difference is that any variables that are bound in the context of the rule, take their binding from the context, rather then being universally quantified.
Thus, a dynamic rule instance can be thought of as having the context variables replaced by the corresponding terms from the context.

For example, the following strategy `DefineInlineCall` defines the dynamic rule `InlineCall`:

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
The construct `{| $Id ... : $Strategy |}` limits the availability of a dynamic rule defined within the brackets to that scope.
After exiting the scope, the state of the dynamic rule definitions before the scope is restored.

```stratego
  inline-functions :
    Let(dec1*, e1) -> Let(dec2*, e2)
    with {| InlineCall
          : <map()> dec1* => dec2*
          |}
    

```


## Multiple Right-Hand Sides


## Dependent Dynamic Rules

Dependent dynamic rules[@OlmosV05].

## References

\bibliography
