---
title: "Custom configuration"
---
# How to provide a custom configuration

There are several valid reasons why the configuration specified in `metaborg.yaml` should be overridden or completely ignored. This quick how-to will show the high-level steps to provide a custom configuration in code for a Spoofax 2 project.



## Override `read()` method
To specify your own configuration reader, extend the `AConfigurationReaderWriter` class. The `createNew()` method should create a new empty configuration, whereas the `read()` method reads a configuration from a file in the specified `rootFolder`. The latter we can override to provide our own custom configuration:

```java
@Override
public HierarchicalConfiguration<ImmutableNode> read(Reader reader, @Nullable FileObject rootFolder)
      throws IOException, ConfigurationException {
    final HierarchicalConfiguration<ImmutableNode> config = new BaseHierarchicalConfiguration();
    String folderName = path.getFilename().getBaseName();
    LanguageVersion version = new LanguageVersion(0, 1, 0, "-SNAPSHOT");

    // Basic properties
    config.setProperty("name", "MyProject");
    config.setProperty("id", new LanguageIdentifier("org.metaborg", folderName, version));

    // Contributions
    config.setProperty("contributions(0).name", "mylang");
    config.setProperty("contributions(0).id", new LanguageIdentifier("org.metaborg", "mylang", version));

    // Stratego
    config.setProperty("language.stratego.format", "jar");

    // SDF
    config.setProperty("language.sdf.enabled", true);
    config.setProperty("language.sdf.sdf2table", "java");

    return config;
}
```


## Override Module
Spoofax 2 uses the Guice dependency injection framework. To use the new configuration reader, override the `MetaborgModule` class `bindConfigMisc()` method:

```java
@Override
protected void bindConfigMisc() {
    bind(AConfigurationReaderWriter.class)
    .to(MyCustomConfigurationReaderWriter.class)
    .in(Singleton.class);
}
```

