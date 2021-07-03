# Strategy Combinators

A _strategy expression_ combines the application of rules using _strategy combinators_.


## Sequential Combinators

### Identity and Failure

```stratego
id
fail
```

The _identity_ strategy `id` always succeeds and behaves as the identity function on terms.
The _failure_ strategy `fail` always fails.
The operations have no side effects.

### Sequential Composition

```stratego
$StrategyExp; $StrategyExp
```

The _sequential composition_ `s1 ; s2` of the strategies `s1` and `s2` first applies the strategy `s1` to the subject term and then `s2` to the result of that first application.
The strategy fails if either `s1` or `s2` fails.

Properties.
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

Example.
Consider the following rewrite rules.

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

The _left choice_ or _deterministic choice_ `s1 <+ s2` tries to apply `s1` and `s2` in that order.
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

Example.
The typical use of left choice is to create a composite strategy trying one from several possible transformations.
If the strategies that are composed are mutually exclusive, that is, don’t succeed for the same terms, their sum is a transformation that (deterministically) covers a larger set of terms.
For example, consider the following two rewrite rules:

```stratego
PlusAssoc : Plus(Plus(e1, e2), e3) -> Plus(e1, Plus(e2, e3))
PlusZero  : Plus(Int("0"), e) -> e
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
  Plus(Plus(Var("x"),Int("42")),Int("3")) =>
  Plus(Var("x"),Plus(Int("42"),Int("3")))
```

Example. An application of `<+` in combination with `id` is the reflexive closure of a strategy `s`:

```stratego
try(s) = s <+ id
```

The user-defined strategy combinator try tries to apply its argument strategy `s`, but if that fails, just succeeds using `id`.


### Guarded Left Choice

```stratego
$StrategyExp < $StrategyExp + $StrategyExp
```

With the _guarded_ left choice operator `s1 < s2 + s3`, if `s1` succeeds `s2` is applied, else `s3` is applied.
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

The `if s1 then s2 else s3 end` construct is like the traditional construct since both branches apply to the original term.
The condition strategy is only used to test if it succeeds or fails, but its transformation effect is undone.
However, the condition strategy `s1` is still applied to the subject term.
The `if s1 then s2 end` strategy is similar; if the condition fails, the strategy succeeds.

The if-then-else-end strategy is just syntactic sugar for a combination of guarded choice and the [where](#where) combinator:

```stratego
    if s1 then s2 else s3 end
==> // transforms to
    where(s1) < s2 + s3
```

The strategy `where(s)` succeeds if `s` succeeds, but returns the original subject term.

Properties.
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

The _switch_ construct is an n-ary branching construct similar to its counter parts in other programming languages.
It is defined in terms of guarded choice.

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

```stratego
$StrategyExp + $StrategyExp
```

The non-deterministic choice operator `s1 + s2` chooses one of the two strategies `s1` or `s2` to apply, such that the one it chooses succeeds.
If both strategies fail, then the choice fails as well.
Operationally the choice operator first tries one strategy, and, if that fails, tries the other.
The order in which this is done is undefined, i.e., arbitrarily chosen by the compiler or runtime system.

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

Note. In the past, the `+` combinator was also used to compose definitions with the same name _within_ a module.
This has been replaced by interpreting such compositions with the textual order of the definitions.
The following transformation illustrates this:

```stratego
module A
  f = s1
  f = s2
=>
f = s1 <+ s2
```


### Fixpoint Recursion

```stratego
rec $Id($StrategyExp)
```

The _fixpoint operator_ `rec x(s)`, which recurses on applications of `x` within `s`.

The rec operator allows the definition of an unnamed strategy expression to be recursive.
For example, in the definition

```stratego
g(s) = foo; rec x(... x ...); bar
```

the strategy between foo and bar is a recursive strategy that does not recurse to `g(s)`.

Alternative.
Originally, the `rec` operator was the only way to define recursive strategies.
Currently, a recursive definition is a normal strategy definition with a recursive call in its body.

```stratego
f(s) = ... f(s) ...
```

The `rec` operator is still in the language in the first place because it is widely used in many existing programs, and in the second place because it can be a concise expression of a recursive strategy, since call parameters are not included in the call.
Furthermore, all free variables remain in scope.

Example.
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

### Building Terms

```stratego
!$Term
```

The build operation `!p` replaces the subject term with the instantiation of the pattern `p` using the bindings from the environment to the variables occurring in `p`.

Example.
The strategy `!Or(And(x, z), And(y, z))` replaces the subject term with the instantiation of `Or(And(x, z), And(y, z))` using bindings to variables `x`, `y` and `z`.

```stratego
!Int("10") => Int("10")
!Plus(Var("a"), Int("10")) => Plus(Var("a"), Int("10"))
```

It is possible to build terms with variables.
A pattern is a term with meta-variables.
The current term is replaced by an instantiation of pattern `p`.

Example.
In a context where `e` is bound to `Var("b")`

```stratego
!Plus(Var("a"),e) => Plus(Var("a"),Var("b"))
```


### Matching Terms

```stratego
?$Term
```

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

Example.
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


### Term Variable Scope

```stratego
{$Id, ... : $StrategyExp}
```

Once a variable is bound it cannot be rebound to a different term.
Thus, when we have applied an anonymous rule once, its variables are bound and the next time it is applied it only succeeds for the same term.
For example, in the next session the second application of the rule fails, because `e2` is bound to `Int("3")` and does not match with `Var("b")`.

```stratego
<?Plus(e1, e2)! Plus(e2, e1))>
  Plus(Var("a"), Int("3")) => Plus(Int("3"), Var("a"))
  // e1 is bound to Var("a")
  // e2 is bound to Int("3")

<?Plus(e1, e2)! Plus(e2, e1)>
   Plus(Var("a"), Var("b")) // fails
```

To use a variable name more than once Stratego provides term variable scope.
A scope `{x1,...,xn : s}` locally undefines the variables `xi`.
That is, the binding to a variable `xi` outside the scope is not visible inside it, nor is the binding to `xi` inside the scope visible outside it.
For example, to continue the session above, if we wrap the anonymous swap rule in a scope for its variables, it can be applied multiple times.

```stratego
<{e3,e4 : ?Plus(e3,e4); !Plus(e4,e3)}>
   Plus(Var("a"),Int("3")) => Plus(Var("a"),Int("3"))
   // e3 is not bound to a term

<{e3,e4 : ?Plus(e3,e4); !Plus(e4,e3)}>
  Plus(Var("a"),Var("b")) => Plus(Var("b"),Var("a"))
```

Of course we can name such a scoped rule using a strategy definition, and then invoke it by its name:

```stratego
SwapArgs =
  {e1,e2 : ?Plus(e1,e2); !Plus(e2,e1)}

<SwapArgs>
  Plus(Var("a"),Int("3")) => Plus(Int("3"),Var("a"))
```


### Implicit Variable Scope

When using match and build directly in a strategy definition, rather than in the form of a rule, the definition contains free variables.
Strictly speaking such variables should be declared using a scope, that is one should write

```stratego
SwapArgs = {e1,e2 : ?Plus(e1,e2); !Plus(e2,e1)}
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
let SwapArgs = ?Plus(e1,e2); Plus(e2,e1) in ... end
```

While the variables are bound in the enclosing definition, they are not restricted to `SwapArgs` in this case, since in a let one typically wants to use bindings to variables in the enclosing code.


## Combining Match and Build

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

```stratego
($Pattern -> $Pattern)
```

An anonymous rewrite rule `(p1 -> p2)` transforms a term matching `p1` into an instantiation of `p2`.
Such a rule is equivalent to the sequence `?p1; !p2`.

```stratego
<(Plus(e1, e2) -> Plus(e2, e1))>
   Plus(Var("a"), Int("3")) =>
   Plus(Int("3"), Var("a"))
```


### Where

```stratego
where($StrategyExp)
```

The `where(s)` combinator applies `s` to the current term, but restores that term afterwards.
Any bindings to variables are kept, however.

The `where(s)` construct is syntactic sugar for `{x: ?x; s; !x}` with `x` a fresh variable not occurring in `s`.
Thus, the current subject term is saved by binding it to a new variable `x`, then the strategy `s` is applied, and finally, the original term is restored by building `x`.

Example

```stratego
<where(?Plus(Int(i), Int(j)); <addS>(i,j) => k)>
   Plus(Int("14"),Int("3")) => Plus(Int("14"),Int("3"))
   // i is bound to "14"
   // k is bound to "17"
```

### With

```stratego
with(s)
```

The strategy `with(s)` applies `s` on the current subject term and then restores the current subject term.
In other words, `s` is executed solely for its side effects, such as binding variables.
In this respect, with is like `where`.
However, `with(s)` differs in a key way: if the strategy `s` fails, Stratego stops with an error, reporting the strategy that failed.


### Lambda Rules

```stratego
\ $Term -> $Term where $Condition \
```

A _lambda rule_ of the form `\ p1 -> p2 where s \` is an anonymous rewrite rule for which the variables in the left-hand side `p1` are local to the rule, that is, it is equivalent to an expression of the form

```stratego
{x1,...,xn : (p1 -> p2 where s)}
```

with `x1`,…,`xn` the variables of `p1`.
This means that any variables used in `s` and `p2` that do not occur in `p1` are bound in the context of the rule.

Example.

```stratego
<map(\ (x, y) -> x \ )> [(1,2),(3,4),(5,6)] => [1,3,5]
```


### Apply and Match

```stratego
$StrategyExp => $Term
<$StrategyExp> $Term
<$StrategyExp> $Term => $Term
```

The operation `<s> p` captures the notion of applying a strategy to a term, i.e., the scenario `!p; s`.
The operation `s => p` capture the notion of applying a strategy to the current subject term and then matching the result against the pattern `p`, i.e., `s; ?p`.
The combined operation `<s> p1 => p2` thus captures the notion of applying a strategy to a term `p1` and matching the result against `p2`, i.e, `!p1; s; ?p2`.


Example.
The conditional rewrite rule

```stratego
EvalPlus :
  Add(Int(i),Int(j)) -> Int(k)
  where !(i,j); addS; ?k
```

can be reformulated as

```stratego
EvalPlus :
  Add(Int(i),Int(j)) -> Int(k)
  where <addS>(i,j) => k
```


### Assignment

```stratego
$Term := $Term
```

The strategy `p1 := p2` builds `p2` and matches the result against `p1`, i.e. it is equivalent to `!p2; ?p1`.
The strategy is often combined with strategy application into `p1 := <s>p2`, which is equivalent to `<s>p2 => p1` (but more familiar to an audience with an imperative mindset).

For example, consider the following rewrite rule

```stratego
EvalPlus :
  Add(Int(i),Int(j)) -> Int(k)
  with k := <addS>(i,j)
```


### Applying Strategies in Build

```stratego
<$StrategyExp> $Term   // in build pattern
```

In a build pattern, the application `<s>t` applies the strategy `s` to the term `t`, returning the resulting term.

Example.
The constant folding rule

```stratego
EvalPlus :
  Add(Int(i),Int(j)) -> Int(k)
  where <addS>(i,j) => k
```

can be simplified by directly applying the addition in the right-hand side:

```stratego
EvalPlus :
  Add(Int(i),Int(j)) -> Int(<addS>(i,j))
```

Example.
The following definition of the `map(s)` strategy applies a strategy to each term in a list:

```stratego
map(s) : [] -> []
map(s) : [x | xs] -> [<s> x | <map(s)> xs]
```


### Term Wrap

```stratego
<$StrategyExp>    // in build pattern
```

A _term wrap_ is a build strategy `!p[<s>]` containing one or more strategy applications `<s>` that are not applied to a term.
When executing the the build operation, each occurrence of such a strategy application `<s>` is replaced with the term resulting from applying `s` to the current subject term, i.e., the one that is being replaced by the build.

Motivation.
One often write rules of the form `x -> Foo(Bar(x))`, i.e. wrapping a term pattern around the current term.
Using rule syntax this is quite verbose.
The syntactic abstraction of term wraps, allows the concise specification of such little transformations as `!Foo(Bar(<id>))`.

Example.
The following applications illustrate some uses of term wraps:

```stratego
<!(<id>,<id>)> 3 => (3,3)

<(<Fst; inc>,<Snd>)> (3,3) => (4,3)

<!Call(<id>, [])> "foobar" => Call("foobar", [])

mod2 = <mod>(<id>,2)

<mod2> 6 => 0
```

Desugaring.
Term wraps are implemented by translation to a combination of match and build expressions.
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

```stratego
<$StrategyExp>   // in match pattern
```

Term projections are the match dual of term wraps.
Term projections can be used to project a subterm from a term pattern.

Examples.
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

Desugaring.
A match expression `?p[<s>]` is desugared as

```stratego
{x: ?p[x]; <s> x}
```

That is, after the pattern `p[x]` matches, it is reduced to the subterm bound to `x` to which s is applied.
The result is also the result of the projection.
When multiple projects are used within a match the outcome is undefined, i.e., the order in which the projects will be performed can not be counted on.


## Traversal Combinators

Traversal combinators apply strategies to direct subterms of a term and can be combined with other combinators to define full term traversal strategies.


### Congruence Operators

```stratego
$Constructor($StrategyExp, ..., $StrategyExp)
```

A congruence operator applies a strategy to each direct subterm of a specific constructor.
For each n-ary constructor `c` declared in a signature, there is a corresponding congruence operator `c(s1 , ..., sn)`, which applies to terms of the form `c(t1 , ..., tn)` by applying the argument strategies to the corresponding argument terms.
A congruence fails if the application of one the argument strategies fails or if constructor of the operator and that of the term do not match.

Example.
Consider the following signature of expressions:

```stratego
module expressions
signature
  sorts Exp
  constructors
    Plus  : Exp * Exp -> Exp
    Times : Exp * Exp -> Exp
```

The following applications apply the congruence operators `Plus` and `Times` to a term:

```stratego
<Plus(!Var("a"), id)>
  Plus(Int("14"),Int("3")) =>
  Plus(Var("a"),Int("3"))

<Times(id, !Int("42"))>
  Plus(Var("a"),Int("3")) // fails
```

The first application shows how a congruence transforms a specific subterm, that is the strategy applied can be different for each subterm.
The second application shows that a congruence only succeeds for terms constructed with the same constructor.


### Tuple and List Congruences

```stratego
[$StrategExp, ..., $StrategyExp]
[$StrategExp, ..., $StrategyExp | $StrategyExp]
($StrategExp, ..., $StrategyExp)
```

Congruences can also be applied to tuples, `(s1,s2,...,sn)`, and lists, `[s1,s2,...,sn]`.

Example. The definition of a `map(s)` strategy using list congruences:

```stratego
map(s) = [] <+ [s | map(s)]
```

### Visiting All Subterms

```stratego
all($StrategyExp)
```

The `all(s)` strategy transforms a constructor application by applying the parameter strategy `s` to each direct subterm.
An application of `all(s)` fails if the application to one of the subterms fails.

The following example shows how all (1) applies to any term, and (2) applies its argument strategy uniformly to all direct subterms.

```stratego
<all(!Var("a"))>
  Plus(Int("14"), Int("3")) => Plus(Var("a"), Var("a"))

<all(!Var("z"))>
  Times(Var("b"), Int("3")) => Times(Var("z"), Var("z"))
```

Example.
The `bottomup(s)` is defined as

```stratego
bottomup(s) = all(bottomup(s)); s
```

and defines a full traversal over the subject term.


### Visiting One Subterm

```stratego
one($StrategyExp)
```

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

Example.
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


### Visiting Some Subterms

```stratego
some($StrategyExp)
```

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

## Generic Term Deconstruction

```stratego
$Term#($Term)   // in a match pattern
```

The term pattern expression `c#(ts)` used in a match pattern succeeds when applied to a constructor application and matches the constructor name (as a string) to `c` and the list of term arguments to `ts`.


## Generic Term Construction

```stratego
$Term#($Term)   // in a build pattern
```

The term pattern expression `c#(ts)` used in a build pattern succeeds when
`c` constructs a string and `ts` constructs a list of terms.
It then builds the corresponding constructor application `c(ts)`.


## References

Rather than defining rewrite rules and high-level strategies as primitives of the language, Stratego provides _strategy combinators_ as basic building blocks from which these can defined[@VisserBT98].
Thus, Stratego consists of a core language[@VisserB98] and a 'sugar' language defined by reduction to the core language.

!!! warning
    While it useful to understand the constructs defined in this section, their use should be avoided in favour of the higher-level language constructs, such as [rewrite rules](rewrite-rules.md), where possible.


\bibliography
