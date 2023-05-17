# Language File Extensions
The file extensions that the editor should recognize as files belonging to the language definition, are configured in the `language` section `extensions` key of an ESV file. They are specified without a leading dot:

```esv
language

  extensions : ent
```

Multiple extensions can be set with a comma-separated list:

```esv
language

  extensions : ent, entity, entities
```

This will assign for example `foo.ent`, `foo.entity`, and `foo.entities` to the language.

