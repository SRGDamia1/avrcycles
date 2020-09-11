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

<https://www.sphinx-doc.org/en/master/man/sphinx-apidoc.html>

As explained in
<https://www.pythonforthelab.com/blog/documenting-with-sphinx-and-readthedocs/>,
in the section titled "Read The Docs", sphinx-autodoc usually requires creating a virtual environment on *Read the Docs*.

For Sphinx to autodoc a module, it must be able to import the
module. If the module depends on a package that is not installed
by default with Python, the import fails.

For example, the Sphinx build fails if the module it is
documenting imports `numpy` and `numpy` is not installed. The
Sphinx build runs fine on my local machine because `numpy` is
installed. But on the *Read the Docs* server, the automated build
uses a fresh install of Python.

Generate a `requirements.txt` file. First activate the virtual
environment for the project:

```bash
$ . ~/py38/bin/activate
(py38) $
```

Now output a `requirements.txt` file in the `doc` folder:

```bash
(py38) $ cd $project_dir
(py38) $ pip freeze > doc/requirements.txt
```

Tell *Read the Docs* to use a virtual environment and install the
packages in `requirements.txt`:

- click the `Admin` button
- click `Advanced Settings`
- scroll down to `Requirements file`
    - enter the path to the requirements file
    - typical path: `doc/requirements.txt`
- scoll down to `Install Project`
    - check the box to "Install your project inside a virtualenv
      using `setup.py install`"

### Useful references

#### Triple double-quote docstrings

Use triple double-quotes for docstrings. See
<https://www.python.org/dev/peps/pep-0257/>

### Type hints

Use type hints for parameters and attributes.

Example:

```
Parameters
----------
cycles : int
  Number of cycles to wait.
```

See <https://www.python.org/dev/peps/pep-0484/>

#### Links to code object in documentation

Link to the part of the documentation where the particular code
object (module, class, function, etc.) is defined:

```
:py:mod:
:py:func:
:py:class:
```

See
<https://www.sphinx-doc.org/en/master/usage/restructuredtext/domains.html#cross-referencing-python-objects>

#### reST basics

```
# with overline, for parts
* with overline, for chapters
=, for sections
-, for subsections
^, for subsubsections
", for paragraphs
```

See <https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html>

See
<https://rest-sphinx-memo.readthedocs.io/en/latest/ReST.html>

#### Directives

```
.. toctree:

.. code-block:

.. code-block: python
   :caption: filename.py
   :name: file-name (for use with :ref:)

.. seealso:

.. note:

.. warning:
```

See directives:
<https://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html>

See refs (links):
<https://www.sphinx-doc.org/en/master/usage/restructuredtext/roles.html#role-ref>

#### NumPy Style Docstrings

Use NumPy docstrings. This style is much friendlier to people
using pydoc. The pure reST style is a mess to read as raw text.

Use the napolean extension to use NumPy style.

See <https://www.sphinx-doc.org/en/master/usage/extensions/example_numpy.html>

See <https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_numpy.html>

# Guides for writing documentation

https://documentation.divio.com/structure/

## Examples of nice documentation

https://docs.divio.com/en/latest/

https://docs.djangoproject.com/en/3.0/#how-the-documentation-is-organized

http://docs.django-cms.org/en/latest/

https://divio-covid-report.readthedocs-hosted.com/en/latest/
