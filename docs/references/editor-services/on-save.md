# On-Save Handlers
The _on-save_ handler (also known as the compiler strategy) is used to transform files when they are saved in an editor. In an IDE, when a new project is opened, the compiler strategy is also executed on each file in the project, as well as when files change in the background. In a command-line batch compiler setting, it is used to transform all files.

The compiler strategy is configured in an [ESV file](esv.md) with the `on save` option:

```esv
language

  on save : $Strategy
```

The identifier after the colon refers to the Stratego strategy that performs the transformation. This strategy must have the exact same signature as the one for [actions](menus.md).

For example:

```esv
language

  on save : compile-file
```
