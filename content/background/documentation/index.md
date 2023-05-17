# Documentation
This section explains the documentation's technology and structure, and how you can contribute.


## Technology
This documentation uses [MkDocs](https://www.mkdocs.org/), a fast and simple static site generated that's geared towards building project documentation from [Markdown](https://daringfireball.net/projects/markdown/) files. In particular, this website uses [MkDocs Material](https://squidfunk.github.io/mkdocs-material/), which provides a clean look, easy customization, and many features for technical documentation.


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
