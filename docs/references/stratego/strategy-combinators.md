# Strategy Combinators

Rather than defining rewrite rules and high-level strategies as primitives of the language, Stratego provides _strategy combinators_ as basic building blocks from which these can defined[@VisserBT98].
Thus, Stratego consists of a core language[@VisserB98] and a 'sugar' language defined by reduction to the core language.

!!! warning
    While it useful to understand the constructs defined in this and the next sections, their use should be avoided in favour of the higher-level language constructs such as [rewrite rules](../rules/rewrite-rules.md) where possible.

## Sequential Combinators

### Identity and Failure

```stratego
id
fail
```

The most basic operations in Stratego are `id` and `fail`.
The identity strategy `id` always succeeds and behaves as the identity function on terms.
The failure strategy `fail` always fails.
The operations have no side effects.

### Sequential Composition

```stratego
$StrategyExp; $StrategyExp
```

The sequential composition `s1 ; s2` of the strategies `s1` and `s2` first applies the strategy `s1` to the subject term and then `s2` to the result of that first application.
The strategy fails if either `s1` or `s2` fails.

Sequential composition is associative.
Identity is a left and right unit for sequential composition; since `id` always succeeds and leaves the term alone, it has no additional effect to the strategy that it is composed with.
Failure is a left zero for sequential composition; since `fail` always fails the next strategy will never be reached.
This leads to the following equations:

```stratego
(s1; s2) ; s3 = s1; (s2; s3)

id; s = s

s; id = s

fail; s = fail
```

However, not for all strategies `s` we have that failure is a right zero for sequential composition:

```stratego
s ; fail = fail   // is not a law
```

Although the composition `s; fail` will always fail, the execution of `s` may have side effects that are not performed by `fail`.
For example, consider printing a term in `s`.

As an example of the use of sequential composition consider the following rewrite rules.

```stratego
A : P(Z(),x) -> x
B : P(S(x),y) -> P(x,S(y))
```

The following applications shows the effect of first applying `B` and then `A`:

```stratego
<B> !P(S(Z()), Z()) => P(S(Z),Z)

<A> P(Z,S(Z)) => S(Z)
```

Using the sequential composition of the two rules, this effect can be achieved ‘in one step’:

```stratego
<B; A> !P(S(Z()),Z()) => S(Z)
```

The following application shows that the application of a composition fails if the second strategy in the composition fails to apply to the result of the first:

```stratego
<B; B> !P(S(Z()),Z()) // fails
```

### Left Choice

```stratego
$StrategyExp <+ $StrategyExp
```

Choosing between rules to apply is achieved using one of several choice combinators, all of which are based on the guarded choice combinator.
The common approach is that failure to apply one strategy leads to backtracking to an alternative strategy.

The left choice or deterministic choice `s1 <+ s2` tries to apply `s1` and `s2` in that order.
That is, it first tries to apply `s1`, and if that succeeds the choice succeeds.
However, if the application of `s1` fails, `s2` is applied to the original term.

Properties.
Left choice is associative.
Identity is a left zero for left choice; since id always succeeds, the alternative strategy will never be tried.
Failure is a left and right unit for left choice; since fail always fails, the choice will always backtrack to the alternative strategy, and use of fail as alternative strategy is pointless.

```stratego
(s1 <+ s2) <+ s3 = s1 <+ (s2 <+ s3)

id <+ s  = id

fail <+ s = s

s <+ fail = s
```

However, identity is not a right zero for left choice.
That is, not for all strategies s we have that

```stratego
s <+ id =  s    // is not a law
```

The expression `s <+ id` always succeeds, even (especially) in the case that `s` fails, in which case the right-hand side of the equation fails of course.

Local Backtracking.
The left choice combinator is a local backtracking combinator.
That is, the choice is committed once the left-hand side strategy has succeeded, even if the continuation strategy fails.
This is expressed by the fact that the property

```stratego
(s1 <+ s2); s3 = (s1; s3) <+ (s2; s3)    // is not a law
```

does not hold for all `s1`, `s2`, and `s3`.
The difference is illustrated by the following applications:

```stratego
<(B <+ id); B> P(S(Z),Z) // fails

<(B; B) <+ (id; B)> P(S(Z()),Z()) => P(Z,S(Z))
```

In the application of `(B <+ id); B`, the first application of `B` succeeds after which the choice is committed.
The subsequent application of `B` then fails.
This is equivalent to first applying `(B <+ id)` and then applying `B` to the result.
The application of `(B; B) <+ (id; B)`, however, is successful; the application of `B; B` fails, after which the choice backtracks to `id; B`, which succeeds.

### Choosing between Transformations.

The typical use of left choice is to create a composite strategy trying one from several possible transformations.
If the strategies that are composed are mutually exclusive, that is, don’t succeed for the same terms, their sum is a transformation that (deterministically) covers a larger set of terms.
For example, consider the following two rewrite rules:

```stratego
PlusAssoc : Plus(Plus(e1, e2), e3) -> Plus(e1, Plus(e2, e3))
PlusZero  : Plus(Int("0"),e) -> e
```

These rules are mutually exclusive, since there is no term that matches the left-hand sides of both rules.
Combining the rules with left choice into `PlusAssoc <+ PlusZero` creates a strategy that transforms terms matching both rules as illustrated by the following applications:

```stratego
<PlusAssoc>
  Plus(Int("0"),Int("3")) // fails

<PlusAssoc <+ PlusZero>
  Plus(Int("0"),Int("3")) => Int("3")

<PlusZero>
  Plus(Plus(Var("x"),Int("42")),Int("3")) // fails

<PlusAssoc <+ PlusZero>
  Plus(Plus(Var("x"),Int("42")),Int("3")) => Plus(Var("x"),Plus(Int("42"),Int("3")))
```

Example. An application of `<+` in combination with `id` is the reflexive closure of a strategy `s`:

```stratego
try(s) = s <+ id
```

The user-defined strategy combinator try tries to apply its argument strategy `s`, but if that fails, just succeeds using `id`.


### Guarded Left Choice

```stratego
$Strategy < $Strategy + $Strategy
```

Sometimes it is not desirable to backtrack to the alternative specified in a choice.
Rather, after passing a guard, the choice should be committed.
This can be expressed using the guarded left choice operator `s1 < s2 + s3`.
If `s1` succeeds `s2` is applied, else `s3` is applied.
If `s2` fails, the complete expression fails; no backtracking to `s3` takes place.

Properties.
This combinator is a generalization of the left choice combinator `<+`.

```stratego
s1 <+ s2 = s1 < id + s2
```

The following laws make clear that the ‘branches’ of the choice are selected by the success or failure of the guard:

```stratego
id < s2 + s3  = s2

fail < s2 + s3 = s3
```

If the right branch always fails, the construct reduces to the sequential composition of the guard and the left branch.

```stratego
s1 < s2 + fail = s1; s2
```

Guarded choice is not associative:

```stratego
(s1 < s2 + s3) < s4 + s5 = s1 < s2 + (s3 < s4 + s5)    // not a law
```

To see why consider the possible traces of these expressions.
For example, when `s1` and `s2` succeed subsequently, the left-hand side expression calls `s4`, while the right-hand side expression does not.

However, sequential composition distributes over guarded choice from left and right:

```stratego
(s1 < s2 + s3); s4 = s1 < (s2; s4) + (s3; s4)

s0; (s1 < s2 + s3) = (s0; s1) < s2 + s3
```

Examples.
The guarded left choice operator is most useful for the implementation of higher-level control-flow strategies.
For example, the negation `not(s)` of a strategy `s`, succeeds if `s` fails, and fails when it succeeds:

```stratego
not(s) = s < fail + id
```

Since failure discards the effect of a (successful) transformation, this has the effect of testing whether `s` succeeds.
So we have the following laws for not:

```stratego
not(id) = fail
not(fail) = id
```

However, side effects performed by `s` are not undone, of course.
Therefore, the following equation does not hold:

```stratego
not(not(s)) = s   // not a law
```

Another example of the use of guarded choice is the restore-always combinator:

```stratego
restore-always(s, r) = s < r + (r; fail)
```

It applies a ‘restore’ strategy `r` after applying a strategy `s`, even if `s` fails, and preserves the success/failure behavior of `s`.
Since `fail` discards the transformation effect of `r`, this is mostly useful for ensuring that some side-effecting operation is done (or undone) after applying `s`.


### If-then-else

```stratego
if $StrategyExp
then
  $StrategyExp
else
  $StrategyExp
end
```

The guarded choice combinator is similar to the traditional if-then-else construct of programming languages.
The difference is that the ‘then’ branch applies to the result of the application of the condition.
Stratego’s `if s1 then s2 else s3 end` construct is more like the traditional construct since both branches apply to the original term.
The condition strategy is only used to test if it succeeds or fails, but it’s transformation effect is undone.
However, the condition strategy `s1` is still applied to the current term.
The `if s1 then s2 end` strategy is similar; if the condition fails, the strategy succeeds.

The if-then-else-end strategy is just syntactic sugar for a combination of guarded choice and the where combinator:

```stratego
    if s1 then s2 else s3 end
==> // transforms to
    where(s1) < s2 + s3
```

The strategy `where(s)` succeeds if `s` succeeds, but returns the original subject term.
The implementation of the `where` combinator is discussed in the section on [matching and building terms](term.md).
The following laws show that the branches are selected by success or failure of the condition:

```stratego
if id   then s2 else s3 end  =  s2

if fail then s2 else s3 end  =  s3
```

The if-then-end strategy is an abbreviation for the if-then-else-end with the identity strategy as right branch:

```stratego
if s1 then s2 end  =  where(s1) < s2 + id
```

Examples. The inclusive or `or(s1, s2)` succeeds if one of the strategies `s1` or `s2` succeeds, but guarantees that both are applied, in the order `s1` first, then `s2`:

```stratego
or(s1, s2) =
  if s1 then try(where(s2)) else where(s2) end
```

This ensures that any side effects are always performed, in contrast to `s1 <\+ s2`, where `s2` is only executed if `s1` fails.
(Thus, left choice implements a short circuit Boolean or.)

Similarly, the following `and(s1, s2)` combinator is the non-short circuit version of Boolean conjunction:

```stratego
and(s1, s2) =
  if s1 then where(s2) else where(s2); fail end
```


### Switch

```stratego
switch s0
  case s1 : s1'
  case s2 : s2'
  ...
  otherwise : sdef
end
```

The switch construct is an n-ary branching construct similar to its counter parts in other programming languages. It is defined in terms of guarded choice. The switch construct has the following form:


The `switch` first applies the `s0` strategy to the current term `t` resulting in a term `t'`.
Then it tries the cases in turn applying each `si` to `t'`.
As soon as this succeeds the corresponding case is selected and `si'` is applied to the `t`, the term to which the switch was applied.
If none of the cases applies, the default strategy `sdef` from the `otherwise` is applied.

The `switch` construct is syntactic sugar for a nested if-then-else:

```stratego
{x : where(s0 => x);
    if <s1> x
    then s1'
    else if <s2> x
        then s2'
        else if ...
            then ...
            else sdef
            end
        end
    end}
```

### Non-Deterministic Choice

The deterministic left choice operator prescribes that the left alternative should be tried before the right alternative, and that the latter is only used if the first fails.
There are applications where it is not necessary to define the order of the alternatives.
In those cases non-deterministic choice can be used.

The non-deterministic choice operator `s1 + s2` chooses one of the two strategies `s1` or `s2` to apply, such that the one it chooses succeeds.
If both strategies fail, then the choice fails as well.
Operationally the choice operator first tries one strategy, and, if that fails, tries the other.
The order in which this is done is undefined, i.e., arbitrarily chosen by the compiler.

The `+` combinator is used to model modular composition of rewrite rules and strategies with the same name, but in different modules.
Multiple definitions with the same name in different modules, are merged into a single definition with that name, where the bodies are composed with `+`.
The following transformation illustrates this:

```stratego
module A
  f = s1
module B   
  f = s2  
module main
  imports A B
=>
  f = s2 + s1
```

This transformation is somewhat simplified; the complete transformation needs to take care of local variables and parameters.

While the `+` combinator is used internally by the compiler for this purpose, programmers are advised not to use this combinator, but rather use the left choice combinator `<+` to avoid surprises.

In the past, the `+` combinator was also used to compose definitions with the same name _within_ a module.
This has been replaced by interpreting such compositions with the textual order of the definitions.
The following transformation illustrates this:

```stratego
module A
  f = s1
  f = s2
=>
f = s1 <+ s2
```


### Recursion

Repeated application of a strategy can be achieved with recursion.
There are two styles for doing this; with a recursive definition or using the fixpoint operator `rec`.
A recursive definition is a normal strategy definition with a recursive call in its body.

```stratego
f(s) = ... f(s) ...
```

Another way to define recursion is using the fixpoint operator `rec x(s)`, which recurses on applications of x within s. For example, the definition

```stratego
f(s) = rec x(... x ...)
```

is equivalent to the one above.
The advantage of the rec operator is that it allows the definition of an unnamed strategy expression to be recursive.
For example, in the definition

```stratego
g(s) = foo; rec x(... x ...); bar
```

the strategy between foo and bar is a recursive strategy that does not recurse to `g(s)`.

Originally, the `rec` operator was the only way to define recursive strategies.
It is still in the language in the first place because it is widely used in many existing programs, and in the second place because it can be a concise expression of a recursive strategy, since call parameters are not included in the call.
Furthermore, all free variables remain in scope.

The `repeat` strategy applies a transformation `s` until it fails.
It is defined as a recursive definition using `try` as follows:

```stratego
try(s)    = s <+ id
repeat(s) = try(s; repeat(s))
```

An equivalent definition using `rec` is:

```stratego
repeat(s) = rec x(try(s; x))
```

## Term Combinators

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


### Building Terms

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


### Matching Terms

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

### Implementing Rewrite Rules

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


### Anonymous Rewrite Rule

An anonymous rewrite rule `(p1 -> p2)` transforms a term matching `p1` into an instantiation of `p2`.
Such a rule is equivalent to the sequence `?p1; !p2`.

```stratego
<(Plus(e1, e2) -> Plus(e2, e1))>
   Plus(Var("a"), Int("3")) => Plus(Int("3"), Var("a"))
```


### Term variable scope

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


### Implicit Variable Scope

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


### Where

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


### Conditional Rewrite Rules

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


### Lambda Rules

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


### Apply and Match

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

### Applying Strategies in Build

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

### Auxiliary Values

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


### Assignment

The assignment combinator `:=` is a variation of apply-and-match with terms on both sides of the assignment.
The strategy `p1 := p2` builds `p2` and matches the result against `p1`, i.e. it is syntactic sugar for `!p2; ?p1`.
The strategy is often combine with strategy application into `p1 := <s>p2`, which is equivalent to `<s>p2 => p1`, but more familiar to an audience with an imperative mindset.

For example, consider the following rewrite rule

```stratego
EvalPlus :
  Add(Int(i),Int(j)) -> Int(k)
  with k := <addS>(i,j)
```

<!-- To sum up, we have actually already seen an example of both `with` and `:=` in the “glue” strategy used to run a Stratego transformation via Editor Services:

```stratego
do-eval:
  (selected, _, _, path, project-path) -> (filename, result)
  with filename := <guarantee-extension(|"eval.aterm")> path
     ; result   := <eval> selected
```

To make the operation of this rule clearer, the two components of the outcome are separated into auxiliary computations in the `with` clause, and these two auxiliaries are implemented as assignments with the `:=` operator.
Moreover, if either the eval strategy fails or if Stratego is unable to compute the proper output filename, there is no point in continuing.
So Stratego will simply terminate immediately and report the error. -->


<!-- ## Wrap and Project

Term wrapping and projection are concise idioms for constructing terms that wrap the current term and for extracting subterms from the current term. -->

### Term Wrap

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


### Term Project

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


## Traversal Combinators

There are many ways to traverse a tree.
For example, a bottom-up traversal, visits the subterms of a node before it visits the node itself, while a top-down traversal visits nodes before it visits children.
One-pass traversals traverse the tree one time, while fixed-point traversals, such as innermost, repeatedly traverse a term until a normal form is reached.

Rather than provide built-in implementations for all traversals needed in transformations, Stratego defines traversals in terms of the primitive ingredients of traversal.
For example, a top-down, one-pass traversal strategy will first visit a node, and then descend to the children of a node in order to recursively traverse all subterms.
Similarly, the bottom-up, fixed-point traversal strategy innermost, will first descend to the children of a node in order to recursively traverse all subterms, then visit the node itself, and possibly recursively reapply the strategy.

Traversal in Stratego is based on the observation[@LuttikV97] that a full term traversal is a recursive closure of a one-step descent, that is, an operation that applies a strategy to one or more direct subterms of the subject term.
By separating this one-step descent operator from recursion, and making it a first-class operation, many different traversals can be defined.

Here we explore the ways in which Stratego supports the definition of traversal strategies.
We start with explicitly programmed traversals using recursive traversal rules. Next, congruences operators provide a more concise notation for such data-type specific traversal rules.
Finally, generic traversal operators support data type independent definitions of traversals, which can be reused for any data type.
Given these basic mechanisms, we conclude with an exploration of idioms for traversal and standard traversal strategies in the Stratego Library.


### Congruence Operators

Congruence operators provide a convenient abbreviation of [traversal with rewrite rules](../../../background/stratego/traversal-with-rules.md).
A congruence operator applies a strategy to each direct subterm of a specific constructor.
For each n-ary constructor `c` declared in a signature, there is a corresponding congruence operator `c(s1 , ..., sn)`, which applies to terms of the form `c(t1 , ..., tn)` by applying the argument strategies to the corresponding argument terms.
A congruence fails if the application of one the argument strategies fails or if constructor of the operator and that of the term do not match.

For example, consider the following signature of expressions:

```stratego
module expressions
signature
  sorts Exp
  constructors
    Int   : String -> Exp
    Var   : String -> Exp
    Plus  : Exp * Exp -> Exp
    Times : Exp * Exp -> Exp
```

The following applications apply the congruence operators `Plus` and `Times` to a term:

```stratego
<Plus(!Var("a"), id)> Plus(Int("14"),Int("3")) => Plus(Var("a"),Int("3"))

<Times(id, !Int("42"))> Plus(Var("a"),Int("3")) // fails
```

The first application shows how a congruence transforms a specific subterm, that is the strategy applied can be different for each subterm.
The second application shows that a congruence only succeeds for terms constructed with the same constructor.

<!-- The import at the start of the session is necessary to declare the constructors used; the definitions of congruences are derived from constructor declarations.
Forgetting this import would lead to a complaint about an undeclared operator:

```stratego
stratego> !Plus(Int("14"),Int("3"))
Plus(Int("14"),Int("3"))
stratego> Plus(!Var("a"), id)
operator Plus/(2,0) not defined
command failed
```
-->

### Defining Traversals with Congruences

Since congruence operators define a one-step traversal for a specific constructor, they capture the pattern of [traversal rules](../../../background/stratego/traversal-with-rules.md).
That is, a traversal rule such as

```stratego
proptr(s) : And(x, y) -> And(<s>x, <s>y)
```

can be written by the congruence `And(s,s)`.
Applying this to the `prop-dnf` program we can replace the traversal rules by congruences as follows:

```stratego
module prop-dnf10
imports prop-rules
strategies
  proptr(s) = Not(s) <+ And(s, s) <+ Or(s, s) <+ Impl(s, s) <+ Eq(s, s)
  propbu(s) = try(proptr(propbu(s))); s
strategies
  dnf = propbu(try(DN <+ (DefI <+ DefE <+ DMA <+ DMO <+ DAOL <+ DAOR); dnf))
  cnf = propbu(try(DN <+ (DefI <+ DefE <+ DMA <+ DMO <+ DOAL <+ DOAR); cnf))
```

<!-- Observe how the five traversal rules have been reduced to five congruences which fit on a single line. -->


### Traversing Tuples and Lists

Congruences can also be applied to tuples, `(s1,s2,...,sn)`, and lists, `[s1,s2,...,sn]`.
A special list congruence is `[]` which ‘visits’ the empty list.
As an example, consider again the definition of `map(s)` using recursive traversal rules:

```stratego
map(s) : [] -> []
map(s) : [x | xs] -> [<s> x | <map(s)> xs]
```

Using list congruences we can define this strategy as:

```stratego
map(s) = [] <+ [s | map(s)]
```

The `[]` congruence matches an empty list.
The `[s | map(s)]` congruence matches a non-empty list, and applies `s` to the head of the list and `map(s)` to the tail.
Thus, `map(s)` applies `s` to each element of a list:

```stratego
<map(inc)> [1,2,3] => [2,3,4]
```

Note that `map(s)` only succeeds if `s` succeeds for each element of the list.
The `fetch` and `filter` strategies are variations on map that use the failure of `s` to list elements.

```stratego
fetch(s) = [s | id] <+ [id | fetch(s)]
```

The `fetch` strategy traverses a list until it finds a element for which `s` succeeds and then stops.
That element is the only one that is transformed.

```stratego
filter(s) = [] + ([s | filter(s)] <+ ?[ |<id>]; filter(s))
```

The `filter` strategy applies `s` to each element of a list, but only keeps the elements for which it succeeds.

```stratego
even = where(<eq>(<mod>(<id>,2),0))

<filter(even)> [1,2,3,4,5,6,7,8] => [2,4,6,8]
```


### Format Checking

Another application of congruences is in the definition of format checkers.
A format checker describes a subset of a term language using a recursive pattern.
This can be used to verify input or output of a transformation, and for documentation purposes.
Format checkers defined with congruences can check subsets of signatures or regular tree grammars.
For example, the subset of terms of a signature in a some normal form.

As an example, consider checking the output of the `dnf` and `cnf` transformations.

```stratego
conj(s) = And(conj(s), conj(s)) <+ s
disj(s) = Or (disj(s), disj(s)) <+ s

// Conjunctive normal form
conj-nf = conj(disj(Not(Atom(id)) <+ Atom(id)))

// Disjunctive normal form
disj-nf = disj(conj(Not(Atom(id)) <+ Atom(id)))
```

The strategies `conj(s)` and `disj(s)` check that the subject term is a conjunct or a disjunct, respectively, with terms satisfying s at the leaves.
The strategies `conj-nf` and `disj-nf` check that the subject term is in conjunctive or disjunctive normal form, respectively.


### Generic Traversal

Using congruence operators we constructed a generic, i.e. transformation independent, bottom-up traversal for proposition terms.
The same can be done for other data types.
However, since the sets of constructors of abstract syntax trees of typical programming languages can be quite large, this may still amount to quite a bit of work that is not reusable across data types; even though a strategy such as bottom-up traversal, is basically data-type independent.
Thus, Stratego provides generic traversal by means of several generic one-step descent operators.
The operator `all`, applies a strategy to all direct subterms.
The operator `one`, applies a strategy to one direct subterm, and the operator `some`, applies a strategy to as many direct subterms as possible, and at least one.


### Visiting All Subterms

The `all(s)` strategy transforms a constructor application by applying the parameter strategy `s` to each direct subterm.
An application of `all(s)` fails if the application to one of the subterms fails.
The following example shows how all (1) applies to any term, and (2) applies its argument strategy uniformly to all direct subterms.
That is, it is not possible to do something special for a particular subterm (that’s what congruences are for).


```stratego
<all(!Var("a"))>
  Plus(Int("14"), Int("3")) => Plus(Var("a"), Var("a"))

<all(!Var("z"))>
  Times(Var("b"), Int("3")) => Times(Var("z"), Var("z"))
```


### Defining Traversals with All

The `all(s)` operator is really the ultimate replacement for the [traversal with rules](../../../background/stratego/traversal-with-rules.md) idiom.
Instead of specifying a rule or congruence for each constructor, the single application of the `all` operator takes care of traversing all constructors.
Thus, we can replace the `propbu` strategy by a completely generic definition of bottom-up traversal.
Consider again the last definition of `propbu`:

```stratego
proptr(s) = Not(s) <+ And(s, s) <+ Or(s, s) <+ Impl(s, s) <+ Eq(s, s)
propbu(s) = try(proptr(propbu(s))); s
```

The role of `proptr(s)` in this definition can be replaced by `all(s)`, since that achieves exactly the same, namely applying `s` to the direct subterms of constructors:

```stratego
propbu(s) = all(propbu(s)); s
```

Moreover, `all` succeeds on any constructor in any signature, so we can also drop the `try` as well, which was there only because `proptr` fails on the ``Atom(...)``, `True()`, and `False()` nodes at the leaves.

However, the strategy now is completely generic, i.e. independent of the particular structure it is applied to.
In the Stratego Library this strategy is called `bottomup(s)`, and defined as follows:

```stratego
bottomup(s) = all(bottomup(s)); s
```

It first recursively transforms the subterms of the subject term and then applies `s` to the result.
Using this definition, the normalization of propositions now reduces to the following module, which is only concerned with the selection and composition of rewrite rules:

```stratego
module prop-dnf11
imports prop-rules
strategies
  dnf = bottomup(try(DN <+ (DefI <+ DefE <+ DMA <+ DMO <+ DAOL <+ DAOR); dnf))
  cnf = bottomup(try(DN <+ (DefI <+ DefE <+ DMA <+ DMO <+ DOAL <+ DOAR); cnf))
```

In fact, these definitions still contain a reusable pattern.
With a little squinting we see that the definitions match the following pattern:

```stratego
dnf = bottomup(try(dnf-rules; dnf))
cnf = bottomup(try(cnf-rules; cnf))
```

In which we can recognize the definition of innermost reduction, which the Stratego Library defines as:

```stratego
innermost(s) = bottomup(try(s; innermost(s)))
```

The `innermost` strategy performs a bottom-up traversal of a term.
After transforming the subterms of a term it tries to apply the transformation `s`.
If successful the result is recursively transformed with an application of `innermost`.
This brings us to the final form for the proposition normalizations:

```stratego
module prop-dnf12
imports prop-rules
strategies
  dnf = innermost(DN <+ DefI <+ DefE <+ DMA <+ DMO <+ DAOL <+ DAOR)
  cnf = innermost(DN <+ DefI <+ DefE <+ DMA <+ DMO <+ DOAL <+ DOAR)
```

Different transformations can be achieved by using a selection of rules and a strategy, which is generic, yet defined in Stratego itself using strategy combinators.


### Visiting One Subterm

The `one(s)` strategy transforms a constructor application by applying the parameter strategy `s` to exactly one direct subterm.
An application of `one(s)` fails if the application to all of the subterms fails.
The following applications illustrate the behavior of the combinator:

```stratego
<one(!Var("a"))>
  Plus(Int("14"), Int("3")) => Plus(Var("a"), Int("3"))

<one(\ Int(x) -> Int(<addS>(x,"1")) \ )>
  Plus(Var("a"), Int("3")) => Plus(Var("a"), Int("4"))

<one(?Plus(_,_))>
  Plus(Var("a"), Int("4")) // fails
```


### Defining Traversals with One

A frequently used application of `one` is the `oncetd(s)` traversal, which performs a left to right depth first search/transformation that stops as soon as s has been successfully applied.

```stratego
oncetd(s) = s <+ one(oncetd(s))
```

Thus, `s` is first applied to the root of the subject term.
If that fails, its direct subterms are searched one by one (from left to right), with a recursive call to `oncetd(s)`.

An application of `oncetd` is the `contains(|t)` strategy, which checks whether the subject term contains a subterm that is equal to t.

```stratego
contains(|t) = oncetd(?t)
```

Through the depth first search of `oncetd`, either an occurrence of `t` is found, or all subterms are verified to be unequal to `t`.

Here are some other one-pass traversals using the one combinator:

```stratego
oncebu(s)  = one(oncebu(s)) <+ s
spinetd(s) = s; try(one(spinetd(s)))
spinebu(s) = try(one(spinebu(s))); s
```

Here are some fixe-point traversals, i.e., traversals that apply their argument transformation exhaustively to the subject term.

```stratego
reduce(s)     = repeat(rec x(one(x) + s))
outermost(s)  = repeat(oncetd(s))
innermostI(s) = repeat(oncebu(s))
```

The difference is the subterm selection strategy.


### Visiting Some Subterms

The `some(s)` strategy transforms a constructor application by applying the parameter strategy `s` to as many direct subterms as possible and at least one. An application of `some(s)` fails if the application to all of the subterms fails.

Some one-pass traversals based on some:

```stratego
sometd(s) = s <+ some(sometd(s))
somebu(s) = some(somebu(s)) <+ s
```

A fixed-point traversal with some:

```stratego
reduce-par(s) = repeat(rec x(some(x) + s))
```


## References

\bibliography




## Generic Term (De)construction

```stratego
$Term#($Term)
```








## References

\bibliography
