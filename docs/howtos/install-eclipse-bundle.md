# Install the Eclipse with Spoofax Plugin Bundle
Install an Eclipse instance with the latest stable release of the Spoofax plugin pre-installed for your platform:

=== "Eclipse with JRE (recommended)"

    Eclipse bundle including the Spoofax plugin _with embedded Java Runtime Environment (JRE)_ (recommended):

    [:fontawesome-brands-apple:<br>macOS Intel (64-bit)]({{ releases.stable.eclipse.bundle_jre.macos.intel }}){ .md-button .md-button--primary .md-button-download }
    [:fontawesome-brands-linux:<br>Linux x64 (64-bit)]({{ releases.stable.eclipse.bundle_jre.linux.x64 }}){ .md-button .md-button--primary .md-button-download }
    [:fontawesome-brands-microsoft:<br>Windows x64 (64-bit)]({{ releases.stable.eclipse.bundle_jre.windows.x64 }}){ .md-button .md-button--primary .md-button-download }
    [:fontawesome-brands-microsoft:<br>Windows x86 (32-bit)]({{ releases.stable.eclipse.bundle_jre.windows.x86 }}){ .md-button .md-button--primary .md-button-download }

=== "Eclipse"

    Eclipse bundle including the Spoofax plugin (_no embedded JRE_):

    [:fontawesome-brands-apple:<br>macOS Intel (64-bit)]({{ releases.stable.eclipse.bundle_nojre.macos.intel }}){ .md-button .md-button--primary .md-button-download }
    [:fontawesome-brands-linux:<br>Linux x64 (64-bit)]({{ releases.stable.eclipse.bundle_nojre.linux.x64 }}){ .md-button .md-button--primary .md-button-download }
    [:fontawesome-brands-microsoft:<br>Windows x64 (64-bit)]({{ releases.stable.eclipse.bundle_nojre.windows.x64 }}){ .md-button .md-button--primary .md-button-download }
    [:fontawesome-brands-microsoft:<br>Windows x86 (32-bit)]({{ releases.stable.eclipse.bundle_nojre.windows.x86 }}){ .md-button .md-button--primary .md-button-download }

[Nightly releases](/nightly.md).

## Troubleshooting

### {{ os.macos }}: "Eclipse" cannot be opened because the developer could not be verified
macOS puts unverified binaries in 'quarantine' and disallows their execution. To remove the `com.apple.quarantine` attribute, do:

```bash
xattr -rc Eclipse.app
```

### Eclipse does not start, or complains about missing Java
Download the Eclipse bundle _with embedded JRE_. Otherwise, ensure you have [a distribution of Java][1] installed. Then in `eclipse.ini`, add a `-vm` line at the top of the file, followed by the path to the Java installation. For example, with [SDKMan!][2] on macOS:

```
-vm
/Users/myusername/.sdkman/candidates/java/current/jre/lib/jli/libjli.dylib
```


[1]: https://adoptopenjdk.net/
[2]: https://sdkman.io/
