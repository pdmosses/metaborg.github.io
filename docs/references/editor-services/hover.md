# Hover Tooltips
Hover tooltips show a textual tooltip with extra information, when hovering part of the text. Hover tooltips are created by a Stratego strategy, but are configured in an [ESV file](esv.md) under the `references` section:

```esv
references

  hover _ : $Strategy
```

For example:

```esv
references

  hover _ : editor-hover
```

The identifier after the colon refers to the Stratego strategy that creates the hover tooltip. The Stratego strategy takes an AST node, and either fails if no tooltip should be produced, or returns a tooltip string.

The string may contain a few simple HTML tag to style the output. The following tags are supported:

- `<br/>` — line break
- `<b>text</b>` — bold
- `<i>text</i>` — italic
- `<pre>code</pre>` — preformatted (code) text

!!! note ""
    Unrecognized HTML tags are stripped from the hover tooltip. Escape angled brackets and ampersands to show them verbatim in the tooltip.
