# Reference Resolution
Reference resolution takes an AST node containing a reference, and tries to resolve it to its definition. The resolution is performed by a Stratego strategy, but is configured in an [ESV file](esv.md) under the `references` section:

```esv
references

  reference _ : $Strategy
```

The identifier after the colon refers to the Stratego strategy that performs the resolution. The Stratego strategy takes an AST node, and either fails if it could not be resolved, or returns an AST node that has an origin location pointing to the definition site.

For example:

```esv
references

  reference _ : editor-resolve
```
