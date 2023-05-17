# Parsing
Parsing language files in an editor is configured in the `language` section of an [ESV file](../esv/esv.md). The syntax is as follows:

```esv
language

  table         : $Path
  start symbols : $Sorts

  line comment  : $String
  block comment : $String * $String
  fences        : $Fences
```

For example:

```esv
language

  table         : target/metaborg/sdf.tbl
  start symbols : File

  line comment  : "//"
  block comment : "/*" * "*/"
  fences        : [ ] ( ) { }
```


### Parse Table
The parse table of your language is set with the `table` key. By default, the parse table of an SDF specification is always produced at `target/metaborg/sdf.tbl`. It is only necessary to change this configuration when a custom parse table is used.

### Start Symbols
The `start symbols` key determine which start symbols to use when an editor is opened. This must be a subset of the start symbols defined in the SDF3 specification of your language.

Multiple start symbols can be set with a comma-separated list:

```esv
language

  start symbols : Start, Program
```

### Comments
The syntax for comments is:

```esv
language

  line comment  : $String
  block comment : $String * $String
```

For example, Java comments are specified as:

```esv
language

  line comment  : "//"
  block comment : "/*" * "*/"
```

The `line comment` key determines how single-line comments are created. It is used by editors to toggle the comment for a single line. For example, in Eclipse, pressing ++ctrl+slash++ (++cmd+slash++ on macOS), respectively comments or uncomments the line. The `block comment` key determines how multi-line comments are created. It is used when a whole block needs to be commented or uncommented. A block comment is described by the two strings denoting the start and end symbols of the block comment respectively.

### Fences
Fences for bracket matching are set as follows:

```esv
language

  fences : $Fences
```

The `fences` key determines which symbols to use and match for bracket matching. A single fence is defined by a starting and closing symbol. Multiple fences can be set with a space-separated list. Fences are used to do bracket matching in text editors.

For example, the default fences in a new Spoofax language project are:

```esv
language

  fences : [ ] ( ) { }
```

!!! warning "Multi-Character Fences"
    Fences can contain multiple characters, but some implementations may not handle bracket matching with multiple fence characters. For example, Eclipse does not handle this case and ignores multi-character fences.
