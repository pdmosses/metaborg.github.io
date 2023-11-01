# Syntax Highlighting
Token-based syntax highlighting is configured in a `colorer` section of an ESV file. Such a section can contain style definitions and styling rules.


## Style Definitions
_Style definitions_ bind an identifier to a style for later reuse, using the syntax:

```esv
  $ID = $Style
```


## Styles
A _style_ specifies a combination of a foreground color, optional background color, and optional font style. Colors are specified as Red-Green-Blue values ranging from 0 (none) to 255 (full). The possible font attributes are:

| Font attribute | Description            |
| -------------- | ---------------------- |
| (none)         | Normal font.           |
| `bold`         | Bold font.             |
| `italic`       | Italic font.           |
| `bold italic`  | Bond and italic font.  |
| `italic bold`  | Same as `bold italic`. |

For example, the following style definitions bind the `red`, `green`, and `blue` colors:

```esv
colorer

  red   = 255 0 0
  green = 0 255 0
  blue  = 0 0 255
```

An optional background color can be set by adding another RGB value:

```esv
colorer

  redWithGreenBackground = 255 0 0 0 255 0
```

The font attributes can be used to make the font bold or italic:

```esv
colorer

  redWithBold   = 255 0 0 bold
  redWithItalic = 255 0 0 italic
  redWithGreenBackgroundWithBoldItalic = 255 0 0 0 255 0 bold italic
```



## Style Rules
_Style rules_ assign a style to matched tokens with syntax:

```esv
$Matcher : $Style
```

Or assigns a previously defined style definition:

```esv
$Matcher : $Ref
```

The left hand side of style rules matches a token, whereas the right hand side assigns a style by referring to a previously defined style definition, or by directly assigning a style. For example, the following matches a token type and references a style definition:

```esv
colorer

  operator : black
```

whereas the following matches a token with a sort and constructor, and directly assigns a style:

```esv
colorer

  ClassBodyDec.MethodDec : 0 255 0
```


## Matchers
There are several ways in which the matcher on the left-hand side of a style rule can be specified: by type, by sort, by constructor, or by sort and constructor.

### Match by Sort and Constructor
The combination of a token sort and constructor can be matched by specifying the `$Sort.$Constructor`. For example:

```
colorer

  ClassBodyDec.MethodDec : yellow
  ClassBodyDec.FieldDec  : red
```

### Match by Constructor
It is also possible to match constructors, regardless of their token sorts, using `_` in place of the sort name. For example:

```esv
colorer

  _.Str     : blue
  _.StrCong : blue
  _.QStr    : blue
  _.QDollar : blue
  _.QBr     : gray
```

### Match by Sort
Additionally, it is possible to match any constructor for a specific sort. For this, just specify the name of the sort, `$Sort`. For example:

```esv
colorer

  ID       : darkblue
  TYPEID   : blue
  JQTYPEID : blue
  PQTYPEID : blue
  FUNCID   : 153 51 0
  JFUNCID  : 153 51 0
  STRING   : 177 47 2
```

### Match by Type
Finally, the following built-in token types can be matched on:

- `identifier` — matches identifiers, found by lexical non-terminals without numbers;
- `keyword` — matches keywords, found by terminals in the syntax definition;
- `layout` — matches layout, such as whitespace and comments, found by layout definition;
- `number` — matches numbers, found by lexical non-terminals with numbers;
- `operator` — matches operations, found by terminals that contain just symbols (no characters);
- `string` — matches strings, found by lexical non-terminals that include quotation marks;
- `unknown` — matches tokens which the parser was unable to infer a type for.
- `var`
- `error`

For example, the following code defines a simple highlighting with token types:

```esv
colorer

  keyword    : 153 51 153
  identifier : black
  string     : 177 47 2
  number     : 17 131 22
  operator   : black
  layout     : 63 127 95 italic
```
