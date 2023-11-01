# Install the Spoofax Eclipse Plugin Manually
Perform a manual installation of the Spoofax plugin in [Eclipse 3.5][1] or newer.

1.  In Eclipse, go to menu _Help_ --> _Install New Software_.
2.  In the _Work with:_ text area, type:

    ```{.text .wrap}
    {{ release.rel.eclipse.repository }}
    ```

    ([Development releases](../../release/develop.md)).

3.  Uncheck _Group items by category_ to make the plugin visible.
4.  Check _Spoofax Eclipse meta-tooling_, _Spoofax Eclipse meta-tooling M2E integration_ and _Spoofax Eclipse runtime_.
5.  Click _Install_ and go through the remaining steps.
6.  Restart Eclipse.

[1]: https://www.eclipse.org/
