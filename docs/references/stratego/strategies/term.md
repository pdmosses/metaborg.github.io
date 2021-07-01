# Term Combinators

[Previously](../rules/rewrite-rules.md) we have presented rewrite rules as basic transformation steps.
However, rules are not atomic transformation actions.
To see this, consider what happens when the rewrite rule

```stratego
DAO : And(Or(x, y), z) -> Or(And(x, z), And(y, z))
```

is applied.
First it matches the subject term against the pattern `And(Or(x, y), z)` in the left-hand side.
This means that a substitution for the variables `x`, `y`, and `z` is sought, that makes the pattern equal to the subject term.
If the match fails, the rule fails.
If the match succeeds, the pattern `Or(And(x, z), And(y, z))` on the right-hand side is instantiated with the bindings found during the match of the left-hand side.
The instantiated term then replaces the original subject term.
Furthermore, the rule limits the scope of the variables occurring in the rule.
That is, the variables `x`, `y`, `z` are local to this rule.
After the rule is applied the bindings to these variables are invisible again.

Thus, rather than considering rules as the atomic actions of transformation programs, Stratego provides their constituents, that is building terms from patterns and matching terms against patterns, as atomic actions, and makes these available to the programmer.
In this section we define the basic actions and their use in the composition of more complex operations such as various flavors of rewrite rules.


## Building Terms

The build operation `!p` replaces the subject term with the instantiation of the pattern `p` using the bindings from the environment to the variables occurring in `p`.
For example, the strategy `!Or(And(x, z), And(y, z))` replaces the subject term with the instantiation of `Or(And(x, z), And(y, z))` using bindings to variables `x`, `y` and `z`.

```stratego
!Int("10") => Int("10")
!Plus(Var("a"), Int("10")) => Plus(Var("a"), Int("10"))
```

It is possible to build terms with variables.
We call this building a term pattern.
A pattern is a term with meta-variables.
The current term is replaced by an instantiation of pattern `p`.

For example, in a context where `e` is bound to `Var("b")`

```stratego
!Plus(Var("a"),e) => Plus(Var("a"),Var("b"))
```


## Matching Terms

Pattern matching allows the analysis of terms.
The simplest case is matching against a literal term.
The match operation `?t` matches the subject term against the term `t`.

```stratego
<?Plus(Var("a"),Int("3"))> Plus(Var("a"),Int("3")) // succeeds
<?Plus(Int("3"),Var("b"))> Plus(Var("a"),Int("3")) // fails
```

Matching against a term pattern with variables binds those variables to (parts of) the current term.
The match strategy `?x` compares the current term (`t`) to variable `x`.
It binds variable `x` to term `t` in the environment.
A variable can only be bound once, or to the same term.

```stratego
<?e> Plus(Var("a"), Int("3")) // binds e to Plus(Var("a"),Int("3"))
<?e> !Int("17")               // fails
```

The general case is matching against an arbitrary term pattern.
The match strategy `?p` compares the current term to a pattern `p`.
It will add bindings for the variables in pattern p to the environment.
The wildcard `_` in a match will match any term.

```stratego
<?Plus(e,_)>Plus(Var("a"),Int("3")) // e is bound to Var("a")
```

Patterns may be non-linear.
Multiple occurrences of the same variable can occur and each occurrence has to match the same term.

```stratego
<?Plus(e,e)> Plus(Var("a"),Int("3")) // fails
<?Plus(e,e)>!Plus(Var("a"),Var("a")) // e is bound to Var("a")
```

Non-linear pattern matching is a way to test equality of terms.
Indeed the equality predicates from the Stratego Library are defined using non-linear pattern matching:

```stratego
equal = ?(x, x)
equal(|x) = ?x
```

The equal strategy tests whether the current term is a a pair of the same terms.
The `equal(|x)` strategy tests whether the current term is equal to the argument term.

```stratego
<equal>("a", "a")               // succeeds
<equal>("a", "b")               // fails
<equal(|Foo(Baz()))> Foo(Bar()) // fails
<equal(|Foo(Bar()))> Foo(Bar()) // succeeds
```

## Implementing Rewrite Rules

Match and build are first-class citizens in Stratego, which means that they can be used and combined just like any other strategy expressions.
In particular, we can implement rewrite rules using these operations, since a rewrite rule is basically a match followed by a build.
For example, consider the following combination of match and build:

```stratego
<?Plus(e1, e2); !Plus(e2, e1)>
   Plus(Var("a"), Int("3")) => Plus(Int("3"), Var("a"))
```

This combination first recognizes a term, binds variables to the pattern in the match, and then replaces the current term with the instantiation of the build pattern.
Note that the variable bindings are propagated from the match to the build.

Stratego provides syntactic sugar for various combinations of match and build.


## Anonymous Rewrite Rule

An anonymous rewrite rule `(p1 -> p2)` transforms a term matching `p1` into an instantiation of `p2`.
Such a rule is equivalent to the sequence `?p1; !p2`.

```stratego
<(Plus(e1, e2) -> Plus(e2, e1))>
   Plus(Var("a"), Int("3")) => Plus(Int("3"), Var("a"))
```


## Term variable scope

Once a variable is bound it cannot be rebound to a different term.
Thus, when we have applied an anonymous rule once, its variables are bound and the next time it is applied it only succeeds for the same term.
For example, in the next session the second application of the rule fails, because `e2` is bound to `Int("3")` and does not match with `Var("b")`.

```stratego
<(Plus(e1, e2) -> Plus(e2, e1))>
  Plus(Var("a"), Int("3")) => Plus(Int("3"), Var("a"))
  // e1 is bound to Var("a")
  // e2 is bound to Int("3")

<(Plus(e1, e2) -> Plus(e2, e1))> Plus(Var("a"), Var("b")) // fails
```

To use a variable name more than once Stratego provides term variable scope.
A scope `{x1,...,xn : s}` locally undefines the variables `xi`.
That is, the binding to a variable `xi` outside the scope is not visible inside it, nor is the binding to `xi` inside the scope visible outside it.
For example, to continue the session above, if we wrap the anonymous swap rule in a scope for its variables, it can be applied multiple times.

```stratego
<{e3,e4 : (Plus(e3,e4) -> Plus(e4,e3))}>
   Plus(Var("a"),Int("3")) => Plus(Var("a"),Int("3"))
   // e3 is not bound to a term

<{e3,e4 : (Plus(e3,e4) -> Plus(e4,e3))}>
  Plus(Var("a"),Var("b")) => Plus(Var("b"),Var("a"))
```

Of course we can name such a scoped rule using a strategy definition, and then invoke it by its name:

```stratego
SwapArgs = {e1,e2 : (Plus(e1,e2) -> Plus(e2,e1))}

<SwapArgs>Plus(Var("a"),Int("3")) => Plus(Int("3"),Var("a"))
```


## Implicit Variable Scope

When using match and build directly in a strategy definition, rather than in the form of a rule, the definition contains free variables.
Strictly speaking such variables should be declared using a scope, that is one should write

```stratego
SwapArgs = {e1,e2 : (Plus(e1,e2) -> Plus(e2,e1))}
```

However, since declaring all variables at the top of a definition is distracting and does not add much to the definition, such a scope declaration can be left out.
Thus, one can write

```stratego
SwapArgs = (Plus(e1,e2) -> Plus(e2,e1))
```

instead.
The scope is automatically inserted by the compiler.
This implies that there is no global scope for term variables.
Of course, variables in inner scopes should be declared where necessary.
In particular, note that variable scope is not inserted for strategy definitions in a let binding, such as

```stratego
let SwapArgs = (Plus(e1,e2) -> Plus(e2,e1)) in ... end
```

While the variables are bound in the enclosing definition, they are not restricted to `SwapArgs` in this case, since in a let you typically want to use bindings to variables in the enclosing code.


## Where

Often it is useful to apply a strategy only to test whether some property holds or to compute some auxiliary result.
For this purpose, Stratego provides the `where(s)` combinator, which applies `s` to the current term, but restores that term afterwards.
Any bindings to variables are kept, however.

```stratego
<where(?Plus(Int(i),Int(j)); <addS>(i,j) => k)>
   Plus(Int("14"),Int("3")) => Plus(Int("14"),Int("3"))
   // i is bound to "14"
   // k is bound to "17"
```

With the match and build constructs `where(s)` is in fact just syntactic sugar for `{x: ?x; s; !x}` with `x` a fresh variable not occurring in `s`.
Thus, the current subject term is saved by binding it to a new variable `x`, then the strategy `s` is applied, and finally, the original term is restored by building `x`.


## Conditional Rewrite Rules

A simple rewrite rule succeeds if the match of the left-hand side succeeds.
Sometimes it is useful to place additional requirements on the application of a rule, or to compute some value for use in the right-hand side of the rule.
This can be achieved with conditional rewrite rules.
A conditional rule `L: p1 -> p2` where `s` is a simple rule extended with an additional computation `s` which should succeed in order for the rule to apply.
The condition can be used to test properties of terms in the left-hand side, or to compute terms to be used in the right-hand side.
The latter is done by binding such new terms to variables used in the right-hand side.

For example, the `EvalPlus` rule in the following session uses a condition to compute the sum of `i` and `j`:

```stratego
EvalPlus:
  Plus(Int(i),Int(j)) -> Int(k)
  where !(i,j); addS; ?k

<EvalPlus> Plus(Int("14"),Int("3")) => Int("17")
```

A conditional rule can be desugared similarly to an unconditional rule.
That is, a conditional rule of the form


```stratego
L : p1 -> p2 where s
```

is syntactic sugar for

```stratego
L = ?p1; where(s); !p2
```

Thus, after the match with `p1` succeeds the strategy `s` is applied to the subject term.
Only if the application of `s` succeeds, is the right-hand side `p2` built.
Note that since `s` is applied within a where, the build `!p2` is applied to the original subject term; only variable bindings computed within `s` can be used in `p2`.

As an example, consider the following constant folding rule, which reduces an addition of two integer constants to the constant obtained by computing the addition.

```stratego
EvalPlus : Add(Int(i),Int(j)) -> Int(k) where !(i,j); addS; ?k
```

The addition is computed by applying the primitive strategy addS to the pair of integers `(i,j)` and matching the result against the variable `k`, which is then used in the right-hand side.
This rule is desugared to


```stratego
EvalPlus = ?Add(Int(i),Int(j)); where(!(i,j); addS; ?k); !Int(k)
```


## Lambda Rules

Sometimes it is useful to define a rule anonymously within a strategy expression.
The syntax for anonymous rules with scopes is a bit much since it requires enumerating all variables.
A lambda rule of the form

```stratego
\ p1 -> p2 where s \
```

is an anonymous rewrite rule for which the variables in the left-hand side `p1` are local to the rule, that is, it is equivalent to an expression of the form

```stratego
{x1,...,xn : (p1 -> p2 where s)}
```

with `x1`,…,`xn` the variables of `p1`.
This means that any variables used in `s` and `p2` that do not occur in `p1` are bound in the context of the rule.

A typical example of the use of an anonymous rule is

```stratego
<map(\ (x, y) -> x \ )> [(1,2),(3,4),(5,6)] => [1,3,5]
```


## Apply and Match

One frequently occuring scenario is that of applying a strategy to a term and then matching the result against a pattern.
This typically occurs in the condition of a rule.
In the constant folding example above we saw this scenario:

```stratego
EvalPlus :
  Add(Int(i),Int(j)) -> Int(k)
  where !(i,j); addS; ?k
```

In the condition, first the term `(i,j)` is built, then the strategy `addS` is applied to it, and finally the result is matched against the pattern `k`.

To improve the readability of such expressions, the following two constructs are provided.
The operation `<s> p` captures the notion of applying a strategy to a term, i.e., the scenario `!p; s`.
The operation `s => p` capture the notion of applying a strategy to the current subject term and then matching the result against the pattern `p`, i.e., `s; ?p`.
The combined operation `<s> p1 => p2` thus captures the notion of applying a strategy to a term `p1` and matching the result against `p2`, i.e, `!p1; s; ?p2`.
Using this notation we can improve the constant folding rule above as

```stratego
EvalPlus :
  Add(Int(i),Int(j)) -> Int(k)
  where <addS>(i,j) => k
```

## Applying Strategies in Build

Sometimes it useful to apply a strategy directly to a subterm of a pattern, for example in the right-hand side of a rule, instead of computing a value in a condition, binding the result to a variable, and then using the variable in the build pattern.
The constant folding rule above, for example, could be further simplified by directly applying the addition in the right-hand side:

```stratego
EvalPlus :
  Add(Int(i),Int(j)) -> Int(<addS>(i,j))
```

This abbreviates the conditional rule above.
In general, a strategy application in a build pattern can always be expressed by computing the application before the build and binding the result to a new variable, which then replaces the application in the build pattern.

Another example is the following definition of the map(s) strategy, which applies a strategy to each term in a list:

```stratego
map(s) : [] -> []
map(s) : [x | xs] -> [<s> x | <map(s)> xs]
```

## Auxiliary Values

As mentioned above, it can be convenient to apply a strategy only to compute some auxiliary result.
Although the `where` construct created to constrain when a rule or strategy may apply (as covered above) can be used for this purpose, often it is better to use the `with` strategy specifically designed with computing auxiliaries in mind.

Specifically, if `s` is any strategy, the strategy `with(s)` executes `s` on the current subject term and then restores the current subject term.
In other words, `s` is executed solely for its side effects, such as binding variables.
In this respect, with is like `where`.
However, `with(s)` differs in a key way: if the strategy `s` fails, Stratego immediately stops with an error, reporting the strategy that failed.
Thus, if `with(s)` is used for auxiliary computations that really should not fail if the transformation is proceeding properly, there is no opportunity for Stratego to backtrack and/or continue applying other strategies, potentially creating an error at a point far removed from the place that things actually went awry.
In short, using `with(s)` instead of `where(s)` any time the intention is not to constrain the applicability of a rule or strategy generally makes debugging your Stratego program significantly easier.

Also as with `where`, we can add a `with` clause to a rewrite rule in exactly the same way.
In other words,

```stratego
L : p1 -> p2 with s
```

is syntactic sugar for

```stratego
L = ?p1; with(s); !p2
```

So as an example, the `where` version of `EvalPlus` above would be better cast as

```stratego
EvalPlus :
  Add(Int(i),Int(j)) -> Int(k)
  with <addS>(i,j) => k
```

because after all, there is no chance that Stratego will be unable to add two integers, and so if the contents of the `with` clause fails it means something has gone wrong – perhaps an `Int` term somehow ended up with a parameter that does not actually represent an integer – and Stratego should quit now.


## Assignment

Furthermore, in setting auxiliary variables often the full power of Stratego strategies is not used, but rather new terms are simply built as needed. Stratego provides an `:=` operator for this purpose; the above rule can be written probably more clearly as

```stratego
EvalPlus :
  Add(Int(i),Int(j)) -> Int(k)
  with k := <addS>(i,j)
```

Technically, `p1 := p2` (which can be used anywhere a strategy is called for, although it is primarily useful in `with` and `where` clauses) is just syntactic sugar for `!p2; ?p1`.
In other words, it builds the value `p2`, and then matches it with `p1`.
In the typical case that `p1` is just a variable, this ends up assigning the result of building the expression `p2` to that variable.

To sum up, we have actually already seen an example of both `with` and `:=` in the “glue” strategy used to run a Stratego transformation via Editor Services:


```stratego
do-eval:
  (selected, _, _, path, project-path) -> (filename, result)
  with filename := <guarantee-extension(|"eval.aterm")> path
     ; result   := <eval> selected
```

To make the operation of this rule clearer, the two components of the outcome are separated into auxiliary computations in the `with` clause, and these two auxiliaries are implemented as assignments with the `:=` operator.
Moreover, if either the eval strategy fails or if Stratego is unable to compute the proper output filename, there is no point in continuing.
So Stratego will simply terminate immediately and report the error.


<!-- ## Wrap and Project

Term wrapping and projection are concise idioms for constructing terms that wrap the current term and for extracting subterms from the current term. -->

## Term Wrap

One often write rules of the form `x -> Foo(Bar(x))`, i.e. wrapping a term pattern around the current term.
Using rule syntax this is quite verbose.
The syntactic abstraction of term wraps, allows the concise specification of such little transformations as `!Foo(Bar(<id>))`.

In general, a term wrap is a build strategy `!p[<s>]` containing one or more strategy applications `<s>` that are not applied to a term.
When executing the the build operation, each occurrence of such a strategy application `<s>` is replaced with the term resulting from applying `s` to the current subject term, i.e., the one that is being replaced by the build.
The following applications illustrate some uses of term wraps:

```stratego
<!(<id>,<id>)> 3 => (3,3)

<(<Fst; inc>,<Snd>)> (3,3) => (4,3)

<!Call(<id>, [])> "foobar" => Call("foobar", [])

mod2 = <mod>(<id>,2)

<mod2> 6 => 0
```

As should now be a common pattern, term projects are implemented by translation to a combination of match and build expressions.
Thus, a term wrap `!p[<s>]` is translated to a strategy expression

```stratego
{x: where(s => x); !p[x]}
```

where `x` is a fresh variable not occurring in `s`.
In other words, the strategy `s` is applied to the current subject term, i.e., the term to which the build is applied.

As an example, the term wrap `!Foo(Bar(<id>))` is desugared to the strategy

```stratego
{x: where(id => x); !Foo(Bar(x))}
```

which after simplification is equivalent to `{x: ?x; !Foo(Bar(x))}`, i.e., exactly the original lambda rule `\x -> Foo(Bar(x))\`.


## Term Project

Term projections are the match dual of term wraps.
Term projections can be used to project a subterm from a term pattern.
For example, the expression `?And(<id>,x)` matches terms of the form `And(t1,t2)` and reduces them to the first subterm `t1`.
Another example is the strategy

```stratego
map(?FunDec(<id>,_,_))
```

which reduces a list of function declarations to a list of the names of the functions, i.e., the first arguments of the `FunDec` constructor.
Here are some more examples:

```stratego
<?[_|<id>]> [1,2,3] => [2,3]

<?Call(<id>, [])> Call("foobar", []) =>  "foobar"
```

Term projections can also be used to apply additional constraints to subterms in a match pattern.
For example, `?Call(x, <?args; length => 3>)` matches only with function calls with three arguments.

A match expression `?p[<s>]` is desugared as

```stratego
{x: ?p[x]; <s> x}
```

That is, after the pattern `p[x]` matches, it is reduced to the subterm bound to `x` to which s is applied.
The result is also the result of the projection.
When multiple projects are used within a match the outcome is undefined, i.e., the order in which the projects will be performed can not be counted on.
