# Nightly Releases
Use the nightly (development) releases of Spoofax only if you want to be on the cutting-edge of Spoofax development.

Choose the _Eclipse Bundle_ installation (recommended), the _Eclipse Plugin_ installation, or the _From Source_ installation:

=== "Eclipse Bundle with JRE (recommended)"
    Download an Eclipse instance with an embedded Java Runtime Environment (JRE) and the latest Spoofax plugin pre-installed for your platform:

    [:fontawesome-brands-apple:<span class="small-icons">+ :fontawesome-brands-java:</span><br>macOS Intel (64-bit)]({{ release.dev.eclipse.install.jvm.macos_64 }}){ .md-button .md-button--primary .md-button-download }
    [:fontawesome-brands-linux:<span class="small-icons">+ :fontawesome-brands-java:</span><br>Linux x64 (64-bit)]({{ release.dev.eclipse.install.jvm.linux_64 }}){ .md-button .md-button--primary .md-button-download }
    [:fontawesome-brands-microsoft:<span class="small-icons">+ :fontawesome-brands-java:</span><br>Windows x64 (64-bit)]({{ release.dev.eclipse.install.jvm.windows_64 }}){ .md-button .md-button--primary .md-button-download }
    [:fontawesome-brands-microsoft:<span class="small-icons">+ :fontawesome-brands-java:</span><br>Windows x86 (32-bit)]({{ release.dev.eclipse.install.jvm.windows_32 }}){ .md-button .md-button--primary .md-button-download }

    [Installation instructions](howtos/install-eclipse-bundle.md).

=== "Eclipse Bundle"
    Download an Eclipse instance (without JRE) and the latest Spoofax plugin pre-installed for your platform:

    [:fontawesome-brands-apple:<br>macOS Intel (64-bit)]({{ release.dev.eclipse.install.macos_64 }}){ .md-button .md-button--primary .md-button-download }
    [:fontawesome-brands-linux:<br>Linux x64 (64-bit)]({{ release.dev.eclipse.install.linux_64 }}){ .md-button .md-button--primary .md-button-download }
    [:fontawesome-brands-microsoft:<br>Windows x64 (64-bit)]({{ release.dev.eclipse.install.windows_64 }}){ .md-button .md-button--primary .md-button-download }
    [:fontawesome-brands-microsoft:<br>Windows x86 (32-bit)]({{ release.dev.eclipse.install.windows_32 }}){ .md-button .md-button--primary .md-button-download }

    [Installation instructions](howtos/install-eclipse-bundle.md).

=== "Eclipse Plugin"
    Perform a manual installation of the Spoofax plugin in [Eclipse 3.5][1] or newer through the update site:

    ```{.text .wrap}
    {{ release.dev.eclipse.repository }}
    ```

    [Installation instructions](howtos/install-eclipse-plugin-manually.md).

=== "From Source"
    Use [Git][1] to clone the [Spoofax Github repository][2]:

    === "HTTPS"

        ```{.text .wrap}
        git clone https://github.com/metaborg/spoofax-releng.git
        ```

    === "HTTPS"

        ```{.text .wrap}
        git clone git@github.com:metaborg/spoofax-releng.git
        ```

    === "GitHub CLI"

        ```{.text .wrap}
        gh repo clone metaborg/spoofax-releng
        ```

    [Installation instructions](howtos/install-from-source.md).


[1]: https://git-scm.com/
[2]: https://github.com/metaborg/spoofax-releng
