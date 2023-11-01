# Install the Eclipse with Spoofax Plugin Bundle
Install an Eclipse instance with the latest stable release of the Spoofax plugin pre-installed for your platform:

=== "Eclipse with JRE (recommended)"

    Eclipse bundle including the Spoofax plugin _with embedded Java Runtime Environment (JRE)_ (recommended):

    [:fontawesome-brands-apple:<span class="small-icons">+ :fontawesome-brands-java:</span><br>macOS Intel (64-bit)]({{ release.rel.eclipse.install.jvm.macos_64 }}){ .md-button .md-button--primary .md-button-download }
    [:fontawesome-brands-linux:<span class="small-icons">+ :fontawesome-brands-java:</span><br>Linux x64 (64-bit)]({{ release.rel.eclipse.install.jvm.linux_64 }}){ .md-button .md-button--primary .md-button-download }
    [:fontawesome-brands-microsoft:<span class="small-icons">+ :fontawesome-brands-java:</span><br>Windows x64 (64-bit)]({{ release.rel.eclipse.install.jvm.windows_64 }}){ .md-button .md-button--primary .md-button-download }
    [:fontawesome-brands-microsoft:<span class="small-icons">+ :fontawesome-brands-java:</span><br>Windows x86 (32-bit)]({{ release.rel.eclipse.install.jvm.windows_32 }}){ .md-button .md-button--primary .md-button-download }

=== "Eclipse"

    Eclipse bundle including the Spoofax plugin (_no embedded JRE_):

    [:fontawesome-brands-apple:<br>macOS Intel (64-bit)]({{ release.rel.eclipse.install.macos_64 }}){ .md-button .md-button--primary .md-button-download }
    [:fontawesome-brands-linux:<br>Linux x64 (64-bit)]({{ release.rel.eclipse.install.linux_64 }}){ .md-button .md-button--primary .md-button-download }
    [:fontawesome-brands-microsoft:<br>Windows x64 (64-bit)]({{ release.rel.eclipse.install.windows_64 }}){ .md-button .md-button--primary .md-button-download }
    [:fontawesome-brands-microsoft:<br>Windows x86 (32-bit)]({{ release.rel.eclipse.install.windows_32 }}){ .md-button .md-button--primary .md-button-download }

[Development releases](../../release/develop.md).

## Troubleshooting
### Unresolveable build extension: Plugin
When building a Spoofax project, if you get this error:

```
Could not download sources or javadoc
Could not read maven project
Some problems were encountered while processing the POMs:
[ERROR] Unresolveable build extension: Plugin
Could not find artifact com.sun:tools.jar:1.8.0 at specified path Spoofax.app/jre/Contents/Home/../lib/tools.jar
```

Then you have used the embedded JRE on an ARM macOS, which is not supported.
See [how to install Spoofax on macOS M1/M2](install-spoofax-on-macos-arm.md) for details.


### {{ os.macos }}: "Eclipse" cannot be opened because the developer could not be verified
macOS puts unverified binaries in 'quarantine' and disallows their execution. To remove the `com.apple.quarantine` attribute, do:

```bash
xattr -rc Eclipse.app
```

### Eclipse does not start, or complains about missing Java
Download the Eclipse bundle _with embedded JRE_. Otherwise, ensure you have [a distribution of Java][1] installed. Then in `eclipse.ini`, add a `-vm` line at the top of the file, followed by the path to the Java installation. For example, with [SDKMan!][2] on macOS:

```
-vm
/Users/myusername/.sdkman/candidates/java/current/lib/jli/libjli.dylib
```


[1]: https://adoptopenjdk.net/
[2]: https://sdkman.io/
