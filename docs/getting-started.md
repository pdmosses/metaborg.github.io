# Getting started
The quickest way to get started with Spoofax by downloading an instance of Eclipse with the latest release. Alternatively, you can install the Spoofax plugin into an existing Eclipse instance, use [Homebrew][2] on macOS, or download and build Spoofax from source.

## Installation
The recommended way to get started with Spoofax is to download an [Eclipse][1] instance with the latest Spoofax plugin. The plugin also includes the Spoofax meta-languages. Alternatively, you can install the Spoofax plugin into an existing Eclipse instance, or download and build Spoofax from source. Choose the _Eclipse Bundle_ installation (recommended) or the _Eclipse Plugin_ installation:

=== "Eclipse Bundle"
    Download an Eclipse instance with an embedded Java Runtime Environment (JRE) and the latest Spoofax plugin pre-installed for your platform:

    [:fontawesome-brands-apple:<span class="small-icons">+ :fontawesome-brands-java:</span><br>macOS Intel (64-bit)]({{ release.rel.eclipse.install.jvm.macos_64 }}){ .md-button .md-button--primary .md-button-download }
    [:fontawesome-brands-linux:<span class="small-icons">+ :fontawesome-brands-java:</span><br>Linux x64 (64-bit)]({{ release.rel.eclipse.install.jvm.linux_64 }}){ .md-button .md-button--primary .md-button-download }
    [:fontawesome-brands-microsoft:<span class="small-icons">+ :fontawesome-brands-java:</span><br>Windows x64 (64-bit)]({{ release.rel.eclipse.install.jvm.windows_64 }}){ .md-button .md-button--primary .md-button-download }
    [:fontawesome-brands-microsoft:<br>Windows x86 (32-bit)]({{ release.rel.eclipse.install.jvm.windows_32 }}){ .md-button .md-button--primary .md-button-download }

    [Installation instructions](howtos/installation/install-eclipse-bundle.md).

    [Download Eclipse with Spoofax without an embedded JRE](howtos/installation/install-eclipse-bundle.md).

    [Development releases](release/develop.md).

=== "Eclipse Plugin"
    Perform a manual installation of the Spoofax plugin in [Eclipse 3.5][1] or newer through the update site:

    ```{.text .wrap}
    {{ release.rel.eclipse.repository }}
    ```

    [Installation instructions](howtos/installation/install-eclipse-plugin-manually.md).

=== "Homebrew ({{ os.macos }})"
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


## Quick Start
Once installed, create a new Spoofax project:

1.  Right-click the _Package Explorer_, choose _New_ --> _Project_, and select _Spoofax Language project_ from the _Spoofax_ category.
2.  Provide a name for your new language and click _Finish_.
3.  Select the created language project and press ++ctrl+alt+b++ (++cmd+alt+b++ on macOS) to build the project.
4.  Create a new file with the extension registered to your language to test it.
5.  Follow one of the [tutorials](/tutorials/) to learn more.

!!! tip "Finding the filename extension of your language"
    If you didn't explicitly specify a filename extension for your language, it is derived from the language name. You can find the filename extension for your language in `editor/Main.esv` at the `extensions` property.


[1]: https://www.eclipse.org/
[2]: https://brew.sh/
