# Development Releases
Use the development (nightly) releases of Spoofax only if you want to be on the cutting-edge of Spoofax development.

Choose the _Eclipse Bundle_ installation (recommended), the _Eclipse Plugin_ installation, or the _From Source_ installation:

=== "Eclipse Bundle"
    Download an Eclipse instance with an embedded Java Runtime Environment (JRE) and the latest Spoofax plugin pre-installed for your platform:

    [:fontawesome-brands-apple:<br>macOS Intel (64-bit)]({{ releases.nightly.eclipse.bundle_jre.macos.intel }}){ .md-button .md-button--primary .md-button-download }
    [:fontawesome-brands-linux:<br>Linux x64 (64-bit)]({{ releases.nightly.eclipse.bundle_jre.linux.x64 }}){ .md-button .md-button--primary .md-button-download }
    [:fontawesome-brands-microsoft:<br>Windows x64 (64-bit)]({{ releases.nightly.eclipse.bundle_jre.windows.x64 }}){ .md-button .md-button--primary .md-button-download }
    [:fontawesome-brands-microsoft:<br>Windows x86 (32-bit)]({{ releases.nightly.eclipse.bundle_jre.windows.x86 }}){ .md-button .md-button--primary .md-button-download }

    [Installation instructions](howtos/install-eclipse-bundle.md).

    [Download Eclipse with Spoofax without an embedded JRE](howtos/install-eclipse-bundle.md).

=== "Eclipse Plugin"
    Perform a manual installation of the Spoofax plugin in [Eclipse 3.5][1] or newer through the update site:

    ```{.text .wrap}
    {{ releases.nightly.eclipse.plugin }}
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
