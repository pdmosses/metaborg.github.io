# Install Spoofax from Source
Perform a manual build and installation of cutting-edge Spoofax from source, by first cloning the [Git][2] repository:

=== "HTTPS"

    ```{.text .wrap}
    git clone https://github.com/metaborg/spoofax-releng.git
    ```

=== "SSH"

    ```{.text .wrap}
    git clone git@github.com:metaborg/spoofax-releng.git
    ```

=== "GitHub CLI"

    ```{.text .wrap}
    gh repo clone metaborg/spoofax-releng
    ```

Then:

1.  Using a terminal, navigate to the root of the `spoofax-releng` repository.
2.  (Optional.) Generate a new Maven `~/.m2/settings.xml` with the Spoofax repository information.
    
    ```bash
    ./b gen-mvn-settings
    ```

    !!! warning "This will overwrite your existing `~/.m2/settings.xml` file!"

3.  Invoke the following command to build Spoofax and its submodules and meta-languages:

    ```bash
    ./b build all
    ```

4.  (Optional.) Generate a new Eclipse instance with the Spoofax plugin embedded into it:

    ```bash
    ./b gen-eclipse --destination Spoofax.app
    ```




[1]: https://www.eclipse.org/
[2]: https://git-scm.com/
[3]: https://github.com/metaborg/spoofax-releng
