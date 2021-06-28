# Documentation
This page explains the documentation's technology and structure, and how you can contribute.

## Technology
This documentation uses [MkDocs](https://www.mkdocs.org/), a fast and simple static site generated that's geared towards building project documentation from Markdown files. In particular, this website uses [MkDocs Material](https://squidfunk.github.io/mkdocs-material/), which provides a clean look, easy customization, and many features for technical documentation.


## Structure
The structure of this documentation follows the [Grand Unified Theory of Documentation](https://documentation.divio.com/) where documentation is split into four categories:

* **Tutorials**: oriented to *learning*, enabling newcomers to get started through a lesson, analogous to teaching a child how to cook.
* **How-Tos**: oriented to a *particular goal*, showing how to solve a specific problem through a series of steps, analogous to a recipe in a cookbook.
* **Reference**: oriented to *information*, describing the machinery through dry description, analogous to an encyclopaedia article.
* **Background**: oriented to *understanding*, explaining through discursive explanation, analogous to an article on culinary social history.


## Contributing
Contributing to the documentation is easy. Quick changes and fixing typos can be done by clicking the :fontawesome-solid-pen: button in the top-right corner of a page, and editing and saving the underlying Markdown file.

More considerable contributions can be made by cloning this repository locally, and editing the Markdown files there. The easiest way to get a _live preview_ (automatically reloading) of your changes, is by installing [Docker](https://www.docker.com/) and executing `#!bash make` from the root directory. This will serve the latest changes to [localhost:8000](http://localhost:8000/).

[:fontawesome-solid-book-open: MkDocs Reference](https://squidfunk.github.io/mkdocs-material/reference/abbreviations/){ .md-button .md-button--primary }
[:fontawesome-solid-book-open: Extensions Reference](https://facelessuser.github.io/pymdown-extensions/extensions/arithmatex/){ .md-button .md-button--secondary }


!!! tip "Adding Pages"
    When you add a new page, don't forget to add it to the `nav` element in the `mkdocs.yml` file, or it will not show up.
    The first page mentioned in `nav` under a section should be some `index.md` (without a title), and will be used as the index page (home page) for that section.

!!! warning "Use Relative Links"
    Use relative links when linking to other Markdown pages. For example, to link to `tutorials` from the `background/index.md` page, write the relative link including the Markdown file, for example:

    ```markdown
    [Tutorials](../tutorials/index.md)
    ```

    Absolute links are not supported, and while they may work locally, they break in production.
    

## Technical Details
The structure of the documentation repository is as follows (hover over any of the files to see its description):

<pre>
📦 /
 ┣ <span title="GitHub CI workflows">📁 .github</span>
 ┣ <span title="Documentation files">📂 docs</span>
 ┃ ┣ <span title="Images, stylesheets, and JavaScript">📂 assets</span>
 ┃ ┃ ┣ <span title="Icon shown in the browser tab">📜 favicon.png</span>
 ┃ ┃ ┣ <span title="Border on the Hero page (dark mode)">📜 hero-border-dark.svg</span>
 ┃ ┃ ┣ <span title="Border on the Hero page (light mode)">📜 hero-border-light.svg</span>
 ┃ ┃ ┣ <span title="Logo shown on the hero page">📜 hero.svg</span>
 ┃ ┃ ┣ <span title="Logo shown in the top bar">📜 logo.svg</span>
 ┃ ┃ ┗ <span title="Extra and overriding CSS styles">📜 styles.css</span>
 ┃ ┣ <span title="Background pages">📂 background</span>
 ┃ ┃ ┗ <span title="Background home page">📜 index.md</span>
 ┃ ┣ <span title="How-Tos pages">📂 howtos</span>
 ┃ ┃ ┗ <span title="How-Tos home page">📜 index.md</span>
 ┃ ┣ <span title="References pages">📂 reference</span>
 ┃ ┃ ┗ <span title="References home page">📜 index.md</span>
 ┃ ┣ <span title="Tutorials pages">📂 tutorials</span>
 ┃ ┃ ┗ <span title="Tutorials home page">📜 index.md</span>
 ┃ ┗ <span title="Hero page (home page)">📜 index.md</span>
 ┣ <span title="Theme overrides">📁 overrides</span>
 ┃ ┣ <span title="Hero template page (home page)">📜 index.html</span>
 ┃ ┗ <span title="Main template page (with metadata)">📜 main.html</span>
 ┣ <span title="Git ignore">📜 .gitignore</span>
 ┣ <span title="Dockerfile">📜 Dockerfile</span>
 ┣ <span title="License">📜 LICENSE</span>
 ┣ <span title="Makefile">📜 Makefile</span>
 ┣ <span title="MkDocs Python Requirements">📜 mkdocs_requirements.txt</span>
 ┣ <span title="MkDocs configuration">📜 mkdocs.yml</span>
 ┗ <span title="Readme">📜 README.md</span>
</pre>
