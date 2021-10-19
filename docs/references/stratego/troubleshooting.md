# Stratego Troubleshooting

## UnsupportedClassVersionError: InteropRegisterer
In Eclipse, if you get this error:

```
Caused by: java.lang.UnsupportedClassVersionError:
MyLanguage/strategies/InteropRegisterer has been compiled by a more recent
version of the Java Runtime (class file version 55.0), this version of the
Java Runtime only recognizes class file versions up to 52.0
```

It is caused by Eclipse internally compiling using the wrong Java version. Go to the Eclipse `#!gui Preferences` (++cmd+comma++ on {{os.macos}}), `#!gui Java > Compiler` and set the `#!gui Compiler Compliance Level` to `1.8` (which corresponds to class file version 52.0).