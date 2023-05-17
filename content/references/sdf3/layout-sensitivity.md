# Layout Sensitivity

SDF3 supports definition of layout sensitive syntax by means of low-level layout _constraints_ and high-level layout _declarations_.

!!! note
    If you want to use layout constraints or layout declarations, you should specify the ``jsglr-version: layout-sensitive`` parameter for SDF3, see [configuration](../configuration/).


## Layout Constraints

While we haven't covered layout _constraints_ in this documentation, the paper of Erdweg et al.[@ErdwegRKO12] describes the concepts.


## Layout Declarations

In the paper of Erdweg et al.[@ErdwegRKO12], the authors describe layout constraints in terms of restrictions involving the position of the subtree involved in the constraint (``0``, ``1``, ...), token selectors (``first``, ``left``, ``last`` and ``right``), and position selectors as lines and columns (``line`` and ``col``).

This mechanism allows writing layout constraints to express alignment, offside and indentation rules, but writing such constraints is
rather cumbersome and error prone.
Alternatively, one may write layout constraints using layout _declarations_, which are more declarative specifications and abstract over lines, columns and token selectors as the original layout constraints from the Erdweg et al. paper[@ErdwegRKO12].


### Tree selectors

To specify which trees should be subject to a layout constraint, one may use: tree positions, SDF3 labeled non-terminals, or unique literals that occurs
in the production.
For example:

```
context-free syntax

    Stmt.IfElse = "if" Exp "then" Stmts "else" else:Stmts  {layout(
        indent "if" 3, else &&
        align 3 else &&
        align "if" "else"
    )}
```

In the layout constraint for the production above, ``else`` refers to the tree for the labeled non-terminal ``else:Stmts``, ``"if"`` refers to the tree
corresponding to the ``"if"`` literal and the number 3 correspond to the tree at *position 3* in the parse tree (starting at 0, ignoring trees for ``LAYOUT?``).


### `align`

The layout constraint ``layout(align x y1, ..., yn)`` specifies that the trees indicated by the tree selectors ``yi`` should be aligned with the tree indicated by the tree selector ``x``, i.e., all these trees should start in the same column.
For example, if we consider the production above, the following program is correct according to the `align` constraints:

```python
if x < 0 then
··x = 0
else
··y = 1
```

Whereas, the following program is incorrect because neither the if and else keyword align (``align "if" "else"``), nor the statements in the branches (``align 3 else``):

```python
if x < 0 then
··x = 0
·else
···y = 1
```


### `align-list`

The constraint `align-list` can be used to indicate that all subtrees within a list should be aligned.
That is, a constraint ``layout(align-list x)``, where ``x`` is a tree selector for a list subtree, can be used to enforce such constraint.
For example, consider the following production and its layout constraint:

```
context-free syntax

    Stmt.If = "if" Exp "then" then:Stmt*  {layout(
        align-list then
    )}
```

This constraint indicates that statements inside the list should be aligned.
Therefore, the following program is correct according to this constraint:

```python
if x < 0 then
··x = 0
··y = 4
··z = 2
```

And the following program is invalid, as the second statement is misaligned:

```python
if x < 0 then
··x = 0
···y = 4
    ··z = 2
```


### `offside`

The offside rule is very common in layout-sensitive languages.
It states that all lines after the first one should be further to the right compared to the first line.
For a description of how the offside rule can be modelled with layout constraints, refer to Erdweg et al.[@ErdwegRKO12].
An example of a declarative specification of the offside rule can be seen in the production below:

```
context-free syntax

    Stmt.Assign = <<ID> = <Exp>> {layout(offside 3)}
```

The layout constraint specifies that when the expression in the statement spams multiple lines, all following lines should be indented with
respect to the column where the expression started.
For example, the following program is valid according to this constraint:

```python
x = 4 * 10
·····+ 2
```

However, the following program is not valid, as the second line of the expression starts at the same column as the first line:

```python
x = 4 * 10
····+ 2
```

Note that if the expression is written on a single line, the constraint is also verified.
That is, the following program successfully parses:

```python
    x = 4 * 10 + 2
```

It is also possible to use the offside relation on different trees.
For example, consider the constraint in the following production:

```
context-free syntax

    Stmt.If = "if" Exp "then" then:Stmt*  {layout(
        offside "if" then
    )}
```

This constraint states that all lines (except the first) of the statements in the ``then`` branch should be indented with respect to the ``if`` literal.
Thus, the following program is invalid according to this layout constraint, because the statement ``x = 2`` should be indented with relation to the topmost ``if``.

```python
    if x < 0 then
    ··if y < 0 then
    x = 2
```

In general, an `offside` constraint involving more than a single tree is combined with `indent` constraint to enforce that the column of the first and all subsequent lines should be indented.


### `indent`

An indent constraint indicates that the column of the first line of a certain tree should be further to the right with respect to another tree.
For example, consider the following production:

```
context-free syntax

    Stmt.If = "if" Exp "then" then:Stmt*  {layout(
        indent "if" then
    )}
```

This constraint indicates that the first line of the list of statements should be indented with respect to the ``if`` literal.
Thus, according to this constraint the following program is valid:

```python
if x < 0 then
··x = 2
```

Note that if the list of statements in the then branch spams multiple lines, the constraint does not apply to its subsequent lines.
For example, consider the following program:

```python
if x < 0 then
··x = 2 + 10
* 4
y = 3
```

This program is still valid, since the column of the first line of the first assignment is indented with respect to the if literal.
To indicate that the first and all subsequent lines should be indented, an offside constraint should also be included.

```
context-free syntax

    Stmt.If = "if" Exp "then" then:Stmt*  {layout(
        indent "if" then &&
        offside "if" then
    )}
```

With this constraint, the remainder of the expression ``* 4`` should also be further to the right compared to the "if" literal.
The following program is correct according to these two constraints, since the second line of the first assignment and the second assignment are also indented with respect to the ``if`` literal:

```python
if x < 0 then
··x = 2 + 10
·* 4
·y = 3
```

### `newline-indent`

The newline-indent constraint indicates that a certain tree should both be located on a new line, as well as further to the right with respect to another tree.

For example, consider the following production:

```
context-free syntax

    Exp.If = "if" Exp "then" then:Exp "else" Exp  {layout(
        newline-indent "if" then
    )}
```

This constraint indicates that the "then" branch of the if-then-else expression needs to be on a new line and indented with respect to the "if" keyword. Thus, according to this constraint the following program is valid:

```python
if x < 0 then
··x + 2 else x * 2
```

The newline-indent constraint does not require that the expression is located on the immediate next line, but rather that it is located _below_ the reference tree. Consequently, the following is also allowed:

```python
if x < 0 then


··x + 2
else x * 2
```

Note that the newline-indent constraint is relative to the _first_ character in the reference tree. That means that, given the following syntax:

```
context-free syntax
    Example.Example = a:FooBar b:Baz {layout(newline-indent a b)}
    FooBar.FooBar = <foo bar>
    Baz.Baz = <baz>
```

The following syntax is valid, despite `bar` being indented further than `baz`:

```
foo
····bar
··baz
```

### `single-line`

The single-line constraints indicates that the entirety of the given subtrees must be located on the same line. For example, consider the following production:

```
context-free syntax
    Exp.If = "if" Exp ":" then:Exp "else" Exp {layout(
        single-line "if" ":"
    )}
```

This enforces that both the `if` and `:` tokens need to be on the same line. As a result, the condition expression also needs to be contained on the same line. Thus, the following program is valid for the given constraints:

```python
if x < 3:
  x + 2 else x * 2
```

Note that the entirety of the referenced tree needs to be on the same line. Consider the following syntax:

```
context-free syntax
    Example.Example = a:Baz b:FooBar {layout(single-line a b)}
    FooBar.FooBar = <foo bar>
    Baz.Baz = <baz>
```

With this definition, the following program is invalid, despite `baz` and the start of `foo bar` being on the same line:

```
baz foo
  bar
```

Using the `single-line` constraint without any parameters will add a constraint that the entire production needs to be on a single line. This can be useful as a shorthand when your grammar requires that the entirety of a production is on the same line:

```
context-free syntax
    Exp.Add = <<Exp> + <Exp>> {layout(single-line)}
    // is equivalent to
    Exp.Add = <<a:Exp> + <b:Exp>> {layout(single-line a b)}
```

---

Finally, all these layout declarations can be ignored by the parser and used only when generating the pretty-printer.
To do that, prefix the constraint with `pp-` writing, for example, `pp-offside` or `pp-align`.

\bibliography
