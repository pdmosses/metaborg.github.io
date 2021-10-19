# Origin Tracking

Origin tracking is the idea to build an origin relation between input and output terms of a transformation in a term transformation system (TRS). It was first proposed by Van Deursen et al. in 1993 in the eponymous article[@DeursenKT93]. The origin relation can be used to traverse from a result term, to the term before the final transformation happened. This relation can be followed further, all the way back to the original input term before all transformations. Examples of uses for this relation (from the paper) are: constructing language-specific debuggers, visualising program execution, and associating positional information with messages in error reports. The first two examples relate to using the TRS to implement evaluation (interpretation) of a programming language, where the abstract syntax tree (AST) of a program is a term that is transformed to execute it. The origin relation allows a debugger or visualiser to show the execution one step at a time. The third example uses the origin relation transitively to reach the original AST of a program and extract positional information from it which was left by the process that created the AST (e.g. a parser or projectional editor). 

Spoofax, in particular Stratego inside of Spoofax, can also do some origin tracking. This origin relation is used as a one-to-one relation to the original AST only, as it is mostly used for accessing the positional information on the original AST, left there by the parser. Stratego origin tracking as it is implemented today is rather limited and confusing to users. Therefore this page describes how it works today, what the original paper described, and how origin tracking might be improved in Stratego 2. 

## Origin Tracking in ASF

!!! warning "Caveat Lector"
    This is a summary based on the first and last sections of the paper. The high-level explanation was intuitive so this is based only on that and not the formal definition in the middle.

The TRS used in the paper was the ASF+SDF meta-environment, of which the ASF part, the algebraic specification formalism, was a conditional term transformation system (CRTS). The origin tracking system was a _static_ analysis applied to rewrite rules to find the origin relations between the left-hand side terms and the right-hand side terms. Through a number of rules this system would track relations between contexts, common variables, common subterms, and the redex. Let's quickly go over 

### Common Variables

Because of non-linear rewrite rules, e.g. `plus(X,X) -> mul(2, X)`, an origin relation could be from a term captured by variable `X` and both the subterms of `plus` on the left. That's the only special case, otherwise it's just a matter of the thing captured in variables and used on both sides of the rule have the obvious relation.

### Common Subterms

Common subterms are related. This is not only the case of variables, but also for constants (e.g. `empty-list` in `append(E,empty-list) -> cons(E,empty-list)`), and larger combinations (e.g. `while(Ezp,S-list)` in `ev-stat(while(Ezp,S-list) , Env) -> ev-stat (while (Ezp, S-list), ev-list (S-list, Env) ) when ev-exp(Exp, Env) =  true`). (Capitalized things are variables in ASF). 

### Redex-Contractum

If not related by a previous rule, the left-hand topmost term and righ-hand topmost term are related. For example, the rule `real-const(Char-list) -> real-type` which returns a type for an expression, relates the type `real-type` on the right to the expression `real-const(...)` on the left. 

### Conditional Rewriting

Because ASF is a _conditional_ rewrite system, there can be `when` clauses that bind more variables and deep pattern matches etc. This means that certain deeper terms on the right-hand side may not get an origin, such as the second `seq` and `add` in `trans(plus(E1,E2)) -> seq(trans(El), seq(trans(E2), add))`. 

## Origin Tracking in Stratego

Origin tracking in Stratego is implemented in the runtime. Calling it a dynamic analysis would be generous, it looks more like an afterthought that's hacked in quickly. 

The place where origin tracking is implemented is the runtime of the `all`, `some` and `one` language constructs. These will make an origin relation between _the origin_ of the term on which the construct is applied, and the result term. This is so the origin relation is always directly to the original AST. This works for tuples and constructor applications, where children are actually changed by the given strategy to apply to the children. The construct also work on lists. There is an extra hack where the origin tracking goes one level deeper in lists (directly implemented in `all`, implemented in the `OriginTermFactory` for `some` and `one`). Therefore the Stratego strategy `origin-track-forced(s) = ![<id>]; map(s); ?[<id>]` adds the "redex-contractum" style origin tracking to a strategy `s` (`map` is implemented in terms of `all` in a performance override for the Java implementation of the Stratego runtime). 

So, the reason why origin tracking in Stratego seems to be broken in edge-cases that you can never quite remember, is because it is only applied by generic traversals, mapping over lists, and other strategies that internally use `all`, `some`, or `one`. Still, this approach allowed for a very quick addition of origin tracking to Stratego without a need to change the compiled (for the static analysis), and in fact Stratego and its compiler don't even really know of origins as a thing that terms can have. 

## A Proposal for Improved Origin Tracking in Stratego

Attempting to replicate the static analysis of ASF for Stratego would be a rather large task that would influence the CTree format between the front-end and back-end of the compiler. That format has been stable for a long time, and changing it could have unexpected effects throughout the codebase of Spoofax. It would also require quite some effort to integrate into both the front-end of the compiler and make the corresponding changes to the back-end, check all the code in between can handle the changed CTree format, etc. And we'll inherit the shortcoming of that analysis, in particular how some terms will still not have origins, and other terms have multiple origins. The first is annoying, and we can possibly overcome it, the second is more dangerous as it breaks the interface Spoofax expects of exactly one origin term. 

So instead my proposal has the following properties: (1) all terms get an origin, (2) which origin is still fairly easy to understand, (3) the implementation effort is minimized. The downsides are: (1) origins may be a bit suboptimal in some situations, (2) a certain (hypothetical!) optimisation of Stratego becomes more complicated.

### The proposal: the origin of a newly built term is the current term

To avoid the whole static analysis, changing the CTree format, etc, the origin tracking rule needs to be dead simple. This proposal will allow for origin tracking to be implemented in back-end of the compiler without extra analysis and support in the front-end, side-stepping the CTree format changes. This does mean that we've lost the information on what were strategy and what were rules in the source text of the Stratego program. But we want origin tracking to be defined for even the most basic strategy expressions anyway, and this seems like the most reasonable approach there. With minor changes to the code generation code in the Stratego compiler, we can target already available methods of the `ITermFactory` to set the origin of a newly built term as the current term. 

Desugared rules will have the correct redex-contractum origin relation. Common variable work as expected due to sharing. In the case of non-linear rewrite rules the leftmost occurrence of the variable is the origin. Common subterms will not get the, perhaps expected, origin relation, instead a subterm will be related to the whole term of the left-hand side. Once this rule is established and understood by Stratego users, they will find code patterns to work around with this. The origin term will still be close to the desired one, just higher up in the tree. 

Apart from suboptimal origins for subterms sometimes, there is the question of optimisation, really of semantics. In core Stratego, you could have a sequence of two builds. In general we cannot optimise this to only the second build, because the first can fail if it uses an unbound variable. But now that the current term is relevant for any build that constructs a new term (rather than only a variable), there will be more edge-cases to keep in mind when attempting to optimise sequences of builds. This is not a concern that affects any current optimisations in Stratego though. But it should be noted as the current term and origins are not explicitly mentioned anywhere in the AST of a Stratego program. 

### Performance implications

Estimated performance impact of the changes proposed above should be minimal, but expectations like that should of course be verified. This will require the construction of a general Stratego benchmark, which we currently do not have available (although there is some source code available from some TRS benchmarking contests). The current API of the `ITermFactory` would require that each term build would need an extra method call to track origins. This short method is expected to be inlined by the JIT compiler, but it could be expensive. If that turns out to be the case, the `ITermFactory` interface could be expanded to allow for a single method to build a new term and provide the origin term as well. Some of these methods already exist, but their semantics is rather constrained. Making proper, backward compatible changes that keep bootstrapping in mind should be possible and not particularly challenging. 

## References

\bibliography
