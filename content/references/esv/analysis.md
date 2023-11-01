# Analysis
The analyzer strategy is used to perform static analyses such as name and type analysis, on the AST that a parser produces. An analysis context provides a project-wide store to facilitate multi-file analysis and incrementality. There are four ways to configure the analysis, which set the analyzer strategy with the `observer` and `context` keys in an ESV file.

```esv
language

  context  : $Context
  observer : $Strategy
```

## No Analysis
To completely disable analysis, do not set an observer and set the context to none:

```esv
language

  context : none
```

## Stratego
Stratego-based analysis allows you to implement your analysis in Stratego:

```esv
language

  context  : legacy
  observer : editor-analyze
```

The identifier after the colon refers to the Stratego strategy that performs the analysis. It must take as input a 3-tuple `(ast, path, projectPath)`. As output it must produce a 4-tuple `(ast, error*, warning*, note*)`. The following Stratego code is an example of a strategy that implements this signature:

```stratego
editor-analyze: (ast, path, projectPath) -> (ast', errors, warnings, notes)
  with ast'     := <analyze> ast
     ; errors   := <collect-all(check-error)> ast'
     ; warnings := <collect-all(check-warning)> ast'
     ; notes    := <collect-all(check-note)> ast'
```

## Statix
To use Statix as the meta-language for name and type analysis, use the `editor-analyze` strategy defined in `trans/analysis.str`, annotate it with the `(constraint)` modifier, and set no context:

```esv
language

  observer : editor-analyze (constraint)
```

By default, the Statix analyzer works in single-file mode and does not consider multi-file name resolution. To enable that, add the `(multifile)` modifier:

```esv
language

  observer : editor-analyze (constraint) (multifile)
```
