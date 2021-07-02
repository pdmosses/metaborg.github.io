# Stable Releases
This page lists the stable releases of Spoofax. While this version is recommended for most users, there is also the [development](develop.md) version.

Choose the _Eclipse Bundle_ installation (recommended), the _Eclipse Plugin_ installation, or the _Homebrew_ installation ({{ os.macos }} only):

=== "Eclipse Bundle with JRE (recommended)"
    Download an Eclipse instance with an embedded Java Runtime Environment (JRE) and the latest Spoofax plugin pre-installed for your platform:

    [:fontawesome-brands-apple:<span class="small-icons">+ :fontawesome-brands-java:</span><br>macOS Intel (64-bit)]({{ release.rel.eclipse.install.jvm.macos_64 }}){ .md-button .md-button--primary .md-button-download }
    [:fontawesome-brands-linux:<span class="small-icons">+ :fontawesome-brands-java:</span><br>Linux x64 (64-bit)]({{ release.rel.eclipse.install.jvm.linux_64 }}){ .md-button .md-button--primary .md-button-download }
    [:fontawesome-brands-microsoft:<span class="small-icons">+ :fontawesome-brands-java:</span><br>Windows x64 (64-bit)]({{ release.rel.eclipse.install.jvm.windows_64 }}){ .md-button .md-button--primary .md-button-download }
    [:fontawesome-brands-microsoft:<span class="small-icons">+ :fontawesome-brands-java:</span><br>Windows x86 (32-bit)]({{ release.rel.eclipse.install.jvm.windows_32 }}){ .md-button .md-button--primary .md-button-download }

    [Installation instructions](../howtos/installation/install-eclipse-bundle.md).

=== "Eclipse Bundle"
    Download an Eclipse instance (without JRE) and the latest Spoofax plugin pre-installed for your platform:

    [:fontawesome-brands-apple:<br>macOS Intel (64-bit)]({{ release.rel.eclipse.install.macos_64 }}){ .md-button .md-button--primary .md-button-download }
    [:fontawesome-brands-linux:<br>Linux x64 (64-bit)]({{ release.rel.eclipse.install.linux_64 }}){ .md-button .md-button--primary .md-button-download }
    [:fontawesome-brands-microsoft:<br>Windows x64 (64-bit)]({{ release.rel.eclipse.install.windows_64 }}){ .md-button .md-button--primary .md-button-download }
    [:fontawesome-brands-microsoft:<br>Windows x86 (32-bit)]({{ release.rel.eclipse.install.windows_32 }}){ .md-button .md-button--primary .md-button-download }

    [Installation instructions](../howtos/installation/install-eclipse-bundle.md).

=== "Eclipse Plugin"
    Perform a manual installation of the Spoofax plugin in [Eclipse 3.5][1] or newer through the update site:

    ```{.text .wrap}
    {{ release.rel.eclipse.repository }}
    ```

    [Installation instructions](../howtos/installation/install-eclipse-plugin-manually.md).


=== "Homebrew"
    On _macOS_ Spoofax can be installed easily using [Homebrew][2].

    Install the _latest release_ of Spoofax Eclipse as follows:

    ```bash
    brew tap metaborg/metaborg
    brew install --cask spoofax
    ```

    The optional command-line tools are installed with:

    ```bash
    brew install strategoxt
    ```

    !!! warning "Upgrading the Spoofax cask is not recommended"
        Upgrading the Spoofax cask using `#!bash brew cask upgrade --greedy` will lose all manually installed plugins. It is recommended to use Eclipse update sites to keep Spoofax up-to-date.

[1]: https://git-scm.com/
[2]: https://github.com/metaborg/spoofax-releng
