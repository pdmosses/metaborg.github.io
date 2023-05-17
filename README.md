# Spoofax Documentation

[![Build][badge-build-img]][badge-build-link]
[![Documentation][badge-docs-img]][badge-docs-link]
[![GitHub][badge-github-img]][badge-github-link]

This is the repository for the [Spoofax documentation](https://spoofax.dev/).
This documentation uses [Material for MkDocs].


## Quick Start
To build the pages and see edits live using [Docker](https://www.docker.com/):

```shell
make
```

Or using [Python 3](https://www.python.org/), creating and activating a _virtual environment_ using `virtualenv` (the more featureful ancestor of `venv`, install with `python3 -m pip install virtualenv`):

```shell
virtualenv venv                 # Create a virtual environment
source venv/bin/activate        # Activate the virtual environment

pip install -r requirements.txt # Install dependencies
mkdocs serve                    # Serve the documentation

deactivate                      # Deactivate the virtual environment
```

Navigate to [localhost:8000](http://localhost:8000/) to see the documentation.
The local documentation is automatically reloaded when changes occur.
Changes pushed to the `main` branch are automatically deployed to Github Pages.


## Adding Pages
New pages should be added to the `mkdocs.yml` `nav` element. The first page mentioned under a section header should be some `**/index.md` without a label, and will be used as the index page for that section.


## Updating Dependencies
Using the [pip-check-updates](https://pypi.org/project/pip-check-updates/) tool, you can check the versions of the dependencies. Install in a _virtual environment_:

```shell
pip install pip-check-updates
```

Usage:

```shell
pcu requirements.txt
```

And update the dependencies to their latest versions using:

```shell
pcu -u requirements.txt
```


[MkDocs Material]: https://squidfunk.github.io/mkdocs-material/
[badge-build-link]: https://github.com/metaborg/metaborg.github.io/actions
[badge-build-img]: https://github.com/metaborg/metaborg.github.io/actions/workflows/docs.yml/badge.svg
[badge-docs-link]: https://www.spoofax.dev/
[badge-docs-img]: https://img.shields.io/badge/docs-latest-brightgreen.svg
[badge-github-link]: https://github.com/metaborg/metaborg.github.io/blob/main/LICENSE
[badge-github-img]: https://img.shields.io/github/license/metaborg/metaborg.github.io