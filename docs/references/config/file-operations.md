# Files


## Language File Extensions
The language file extensions are configured in the `language` section `extensions` key of an [ESV file](esv.mb). They are specified without a leading dot:

```esv
language

  extensions : ent
```

Multiple extensions can be set with a comma-separated list:

```esv
language

  extensions : ent, entity, entities
```

This will assign `foo.ent`, `foo.entity`, and `foo.entities` to the language.





- Language
    - File Extensions
    - On-Save