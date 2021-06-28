# Stratego
The Java JAR and CTree files that will be loaded into the Stratego runtime for your language can be configured with the `provider` key in an [ESV file](esv.md):

```esv
language

  provider : $Path
```

The path is a path to a `.jar` or `.ctree` file, relative to the root of the project. For example:

```esv
language

  provider : target/metaborg/stratego.ctree
```

The extension of the provider should match the format in the `metaborg.yaml` file of your language.
Multiple files can be set by setting the key multiple times:

``esv
language

  provider : target/metaborg/stratego.ctree
  provider : target/custom1.jar
  provider : target/custom2.ctree
```

