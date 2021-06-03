# Install the Eclipse with Spoofax Plugin Bundle
Install an Eclipse instance with the Spoofax plugin pre-installed for your platform:


[:fontawesome-brands-apple: macOS Intel 64-bit](http://artifacts.metaborg.org/service/local/repositories/releases/content/org/metaborg/org.metaborg.spoofax.eclipse.dist/2.5.15/org.metaborg.spoofax.eclipse.dist-2.5.15-macosx-x64-jre.tar.gz){ .md-button .md-button--primary }

[:fontawesome-brands-linux: Linux x64 (64-bit)](http://artifacts.metaborg.org/service/local/repositories/releases/content/org/metaborg/org.metaborg.spoofax.eclipse.dist/2.5.15/org.metaborg.spoofax.eclipse.dist-2.5.15-linux-x64-jre.tar.gz){ .md-button .md-button--primary }

[:fontawesome-brands-windows: Windows x64 (64-bit)](http://artifacts.metaborg.org/service/local/repositories/releases/content/org/metaborg/org.metaborg.spoofax.eclipse.dist/2.5.15/org.metaborg.spoofax.eclipse.dist-2.5.15-windows-x64-jre.zip){ .md-button .md-button--primary }

[:fontawesome-brands-windows: Windows x86 (32-bit)](http://artifacts.metaborg.org/service/local/repositories/releases/content/org/metaborg/org.metaborg.spoofax.eclipse.dist/2.5.15/org.metaborg.spoofax.eclipse.dist-2.5.15-windows-x86-jre.zip){ .md-button .md-button--primary }

## Troubleshooting

### {{ os.macos }}: "Eclipse" cannot be opened because the developer could not be verified
macOS puts unverified binaries in 'quarantine' and disallows their execution. To remove the `com.apple.quarantine` attribute, do:

```bash
xattr -rc Eclipse.app
```

### Eclipse does not start, or complains about missing Java
Ensure you have [a distribution of Java][1] installed. Then in `eclipse.ini`, add a `-vm` line at the top of the file, followed by the path to the Java installation. For example, with SDKMan! on macOS:

```
-vm
/Users/myusername/.sdkman/candidates/java/current/jre/lib/jli/libjli.dylib
```


[1]: https://adoptopenjdk.net/