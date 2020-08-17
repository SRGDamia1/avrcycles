# Read the Docs: a tutorial

I created repository `avrcycles` to learn how to publish
documentation to *Read the Docs*. See the [finished
result](https://avrcycles.readthedocs.io/en/latest/index.html).

*Read the Docs* expects documentation made with Sphinx, so it was
time for me to learn to use
[Sphinx](https://pypi.org/project/Sphinx/) and how it relates to
[Read the Docs](https://docs.readthedocs.io/en/stable/). For more
motivation, see this [Eric Holscher blog
post](https://www.ericholscher.com/blog/2016/mar/15/dont-use-markdown-for-technical-docs/).

## Setup documentation with Sphinx

The Getting Started guide on *Read the Docs* starts with an
introduction to making documentation with Sphinx.

### Install Sphinx

```bash
$ pip install sphinx
```

### Quickstart the documentation

Pick a project to document. Create a `docs` folder in the top level of the project repository:

```bash
$ mkdir docs
```

Setup documentation with `sphinx-quickstart`:

```bash
$ cd docs
$ sphinx-quickstart # launch cmdline UI for basic config
$ vim index.rst # this is the *Read the Docs* homepage!
```

- `index.rst` is *reStructuredText*

### reST syntax:

- see reST syntax guide here:
  <https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html>

TLDR for Markdown users learning reST:

#### lists

```rst
* bullet 1
* bullet 2 continues onto another line
  by using the correct indentation

    * a sub-item is indented as expected
      but, unlike Markdown, must be preceded by
      a blank-line
    * then the next sub-item continues as expected

* bullet 3 continues as part of the list
```

#### italics, bold, monospace

```rst
*inline italics*
**inline bold**
``inline code``
```

### Build documentation as HTML

Build the documentation:

```bash
$ make html
```

Clean the documentation folder:

```bash
$ make clean
```

Clean and build in one invocation:

```bash
$ make clean html
```

### View the documentation in a browser

View the documentation by opening `_build/html/index.html` in a
web browser.

### Pick a better HTML theme

Open `docs/conf.py` and search for `html_theme`.

The default `html_theme` is *alabaster*:

```python
html_theme = "alabaster"
```

There are [a few built-in
themes](https://www.sphinx-doc.org/en/master/usage/theming.html).
For example, the official Python docs use *classic*.

*Read the Docs* offers its own theme:

```bash
$ pip install sphinx-rtd-theme
```

Add to the list of `extensions` in `conf.py`:

```python
extensions = [
        "sphinx_rtd_theme",
]
```

And set the `html_theme`:

```python
html_theme = "sphinx_rtd_theme"
```

With this theme you can also add a logo for the upper-left of the
screen:

```python
html_logo = '_static/logo.png'
html_static_path = ['_static']
```

All paths are relative to the directory with the `conf.py` file.
So `_static` is a folder inside `docs`:

```bash
avrcycles
└── docs
    ├── _static
    │   └── logo.png
    └── conf.py
```

Lastly, Sphinx documentation generated with `sphinx-quickstart`
needs this line added to the `conf.py` file:

```python
master_doc = 'index'
```

This overrides the *Read the Docs* expectation for a file named
`contents.rst`.

### Use Markdown and reST in the same project

Install package `recommonmark` to use *Markdown* and *reST*
in the same Sphinx documentation build:

```bash
$ pip install recommonmark
```

Add `recommonmark` (not `m2r`) to the list of `extensions` in
`conf.py`:

```python
extensions = ['recommonmark']
```

*Markdown* is easier to read but *reST* is more powerful. Use
*reST* for technical documentation:

<https://www.ericholscher.com/blog/2016/mar/15/dont-use-markdown-for-technical-docs/>

### Publish to *Read the Docs*

Create an account on *Read the Docs* and link it to your GitHub
account.

Import the GitHub repository into *Read the Docs* and Build.

## Make better documentation

Start by modifying index.rst.

See the *Read the Docs* tutorial [starting here](https://sphinx-rtd-tutorial.readthedocs.io/en/latest/build-the-docs.html).

The ideas are summarized below.

### ToC and `.rst` files

`index.rst` is a reStructuredText file. This file, like the
`index.html` that Sphinx builds, is the main page for the
documentation on *Read the Docs*.

This file contains a welcome message and a table of contents.
This is the same table of contents that appears in the left-hand
navigation pane.

```rst
Welcome to avrcycles's documentation!
=====================================

 .. toctree::
    :maxdepth: 2
    :caption: Contents:

    usage
    implementation
    What is AVRA? <avra>
    Link to Project homepage <homepage>
    README on homepage <README>
```

- `.. toctree` is a directive for creating a table of contents
    - the directive ends with a blank line
- each line after the directive corresponds to one or more
  top-level link in the table of contents:
    - the link points to the rendered version of the `.rst` file,
      e.g., the first link is the rendered version of `usage.rst`
    - the link text defaults to the first *section* in the `.rst`
      file
    - if there are multiple sections in one file, that file
      shows up in the ToC as multiple top-level links
    - and since the `maxdepth` is 2, any sub-sections in the
      `.rst` files show as sub-section links in the ToC, but
      sub-sub-sections do not show up in the ToC

It is clear now how the documentation is split up across multiple
files.

The file name, without the .rst extension, goes in the list under
`Contents`. By default, the **name that is displayed** in the
table-of-contents is **the first section name** in the .rst file.

*A section is a heading with = as the underline character.*

To override this default display name, put the filename inside
`<>`, and the preceding text becomes the name displayed in the
table-of-contents.

### Autodoc

In addition to manually writing `.rst` files, Sphinx
auto-generates module documentation with `sphinx-apidoc`.

