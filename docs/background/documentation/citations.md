# Documentation Citations
To cite a paper or work, first ensure the citation is in a bibliography (`.bib`) file in the `/bibliographies/` directory. For example, in the `bibliographies/spoofax.bib` file, we find:

```bib
@inproceedings{KatsV10,
  title = {The {Spoofax} language workbench: rules for declarative specification of languages and {IDEs}},
  author = {Lennart C. L. Kats and Eelco Visser},
  year = {2010},
  doi = {10.1145/1869459.1869497},
  url = {https://doi.org/10.1145/1869459.1869497},
  pages = {444-463},
  booktitle = {Proceedings of the 25th Annual ACM SIGPLAN Conference on Object-Oriented Programming, Systems, Languages, and Applications, OOPSLA 2010},
}
```

??? note "Adding References"
    To add a reference, add it on [Researchr][1] to [the Spoofax bibliography](https://researchr.org/bibliography/metaborg-spoofax/publications). Then on the command-line, invoke the following to regenerate the `spoofax.bib` file:

    ```
    make bib
    ```

!!! warning "Do not change the `spoofax.bib` file manually, it is generated and updated through [Researchr][1]."

Then reference the work like this:

<div class="highlight"><pre id="__code_2"><code>The Spoofax language workbench&lsqb;@KatsV10&rsqb; is vital to declarative language development.</code></pre></div>

Finally, add a place for the bibliography footnotes to be added (usually at the end of the file) by adding the following line to the file:

<div class="highlight"><pre id="__code_2"><code>&bsol;bibliography</code></pre></div>

The line will be rendered as:

> The Spoofax language workbench[@KatsV10] is vital to declarative language development.

And the references will be at the bottom of this page.

!!! tip ""
    If the citation appears rendered as `Spoofax language workbench[^1]`, then you might have forgotten to add a place for the bibliography.

\bibliography

[1]: https://researchr.org/