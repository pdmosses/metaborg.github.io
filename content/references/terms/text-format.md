---
title: "Text Format"
---
# Textual Term Format
This page describes the textual term format used to write terms to files when exchanging terms between applications.

## File Structure
Term files have the extension `.aterm` and are written using UTF-8 encoding.  They start with the root term.  Each term is written such that each subterm is recursively nested within.

The format is described using regular expressions.

## Whitespace
Whitespace is allowed between some tokens. Whitespace is defined as:

```regex
WS = [ \t\r\n]
```

!!! note "Currently, comments are not supported."


## Integer
An integer literal is represented by a sequence of digits.

```regex
Term.Int = [0-9]+ Annos?
```

!!! note "Currently, negative integer values are not supported."

Examples:

```
0
42
8388608
```


## Real
A real literal is represented by a (possibly empty) sequence of digits, a decimal dot `.`, and another sequence of digits, ending with an optional exponent.

```regex
Term.Real = [0-9]* '.' [0-9]+ ( [eE] [0-9]+ )? Annos?
```

!!! note "Currently, negative real values or negative exponents are not supported."

Examples:

```
0.1
13.37
42.0e3
.5
.3333E2
```


## String
A string literal is represented by a sequence of characters between double quotes.  The character may not include double quotes, backslashes, carriage returns, or new lines.  Instead, those characters need to be escaped.  Other characters may be escaped.

```regex
Term.String = '"' ( [^"\\\r\n] | $escape$ )*  '"' Annos?
```

Where `$escape$` is one of:

- `\b`: Backspace (BS, 8).
- `\t`: Horizontal tab (HT, 9).
- `\n`: New line (LF, 10).
- `\f`: Form-feed (FF, 12).
- `\r`: Carriage return (CR, 13).
- `\"`: Literal double quote (`"`, 34).
- `\'`: Literal single quote (`'`, 39).
- `\\`: Literal backslash (`\`, 92).

??? note "Unsupported escapes"
    The following escape codes are not currently supported:

    - `\0`: Null character (NUL, 0).
    - `\a`: Bell (BEL, 7).
    - `\v`: Vertical tab (VT, 11).
    - `\e`: Escape (ESC, 27).
    - `\nnn`: Unicode code point given by octal number _nnn_ (3 octal digits).
    - `\xhh..`: Unicode code point given by hexadecimal number _hh_ (2 or more hexadecimal digits).
    - `\uhhhh`: Unicode code point given by hexadecimal number _hhhh_ (4 hexadecimal digits).
    - `\Uhhhhhhhh`: Unicode code point given by hexadecimal number _hhhhhhhh_ (8 hexadecimal digits).

!!! note "Using other escape sequences than those specified here is an error."

Examples:

```
"foobar"
"\"I have a dream.\" - Martin Luther King Jr."
">>\n[-]\n<<\n[\n  -\n  >>\n  +\n  <<\n]"
```


## Constructor Application
A constructor application is represented by the constructor name, followed the argument list.  The argument list is represented by a comma-separated (possibly empty) sequence of terms, surrounded by parentheses (`( )`).

```regex
Term.Appl = CName WS* '(' WS* (Term WS* (',' WS* Term)*)? WS* ')' Annos?

CName = [a-z\_\-\+\*\$]*
```

!!! note "Empty constructor name is allowed"
    An empty constructor name is allowed.  This represents a _tuple_.

??? note "Unsupported constructor names"
    Currently, constructor names cannot contain a dot `.` or some other special characters. Additionally, constructor names cannot be strings.

!!! note "Currently, trailing comma in the argument list is not supported."

!!! note "Parentheses are required even when the constructor has no arguments."

Examples:

```
Id()
Plus(Int("1"), Int("1"))
_internal(3)
("foobar", 42)
()
```


## List
A list is represented by a comma-separated (possibly empty) sequence of terms, surrounded by square brackets (`[ ]`).

```regex
Term.List = '[' WS* (Term WS* (',' WS* Term)*)? WS* ']' Annos?
```

!!! note "Currently, trailing comma in the argument list is not supported."

Examples:

```
[]
[1, 2, 3]
["a", ["b", ["c"]]]
```


## Annotation
Term annotations are represented by a comma-separated (possibly empty) sequence of terms, surrounded by curly brackets (`{ }`).

```regex
Annos = '{' WS* (Term WS* (',' WS* Term)*)? WS* '}'
```

!!! note "Currently, trailing comma in the argument list is not supported."

!!! note "When the annotations list is empty, the curly brackets may be omitted."

Examples of terms with annotations:

```
0{MyAnno()}
42.0e3{}
"foobar"{IsConstant()}
(){}
Plus(Int("1"), Int("1")){Type("Int"), FreeVars([])}
[1, 2, 3]{1, 2, 3}
```

