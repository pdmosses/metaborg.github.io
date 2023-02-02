---
title: "Internal Links"
---
# How to write internal links
Links to other parts of the documentation should be written as _relative_ links and point to specific Markdown files. For example, to add a link to `tutorials` from the `background/index.md` page, the link should read:

```markdown
[Tutorials](../tutorials/index.md)
```

!!! note ""
    To link to the index page of a section, link to the `index.md` file.

!!! warning "Avoid internal links without `.md`"
    Even if it might seem to work, do not link to an internal page without specifying the `.md` file to link to. For example, do not use `[Background](../background/)`. These links will not work once the documentation has been deployed.

    Additionally, you won't see any warnings about these (possibly broken) links in the console when running `mkdocs` or its Docker image.

!!! warning "Absolute Links are Not Supported"
    Even if it might seem to work, do not link to an internal page using an absolute link. For example, do not use `[Background](/background/index.md)`. These links are not properly converted and will break once the documentation has been deployed.
