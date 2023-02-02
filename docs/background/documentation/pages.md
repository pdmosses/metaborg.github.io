---
title: "Adding Pages"
---
# How to add a new documentation page
To add a new page to the documentation:

1.  Create a [Markdown](https://daringfireball.net/projects/markdown/) (`.md`) file in an appropriate location in the `docs/` folder;
2.  Add the page to the `nav` element in the `mkdocs.yml` file in the root of the repository.

    ??? tip "Overriding the title"
        By default, the title shown in the Table of Contents is the title of the page. To override this, specify a title in the `nav` element explicitly. For example:

        ```yaml
        nav:
          - Home:
            - index.md
            - Installation: getting-started.md
        ```

!!! warning ""
    By convention, the first page mentioned in `nav` under a section should be some `index.md` (without a title), and will be used as the index page (home page) for that section.
