# avrcycles

The *project* is just one Python script: `avrcycles.py`. This was
a quick-fix at work: I was analyzing disassembly to compare
execution time with and without interrupts. I got tired of
manually looking up the cycles times for each instruction was and
adding them together.

`avrcycles.py` defines a parser function to pull the instruction
from each line of code in the `.avra` file to analyze. It then
looks up each instruction in a dictionary and reports the total
number of cycles consumed by the code in the `.avra` file.

In practice, I manually identify a block of assembly that
corresponds to the C code in question, then I paste this block
into a new `.avra` file and run `avrcycles.py` on that file.

The dictionary of instructions in `avrcycles.py` started out as
just the handful of the instructions I needed from the
*Instruction Set Summary* at the end of the ATmega328P datasheet.

Over time, I add to the dictionary as I analyze new assembly code
and encounter instructions I did not include yet. I still don't
have *all* the instructions in here, but I've run this script on
*a lot* of ATmega328P assembly code and have not run into any
missing instructions yet.

# readthedocs

I created repository `avrcycles` to learn how to publish
documentation to *readthedocs*.

*readthedocs* expects documentation made with Sphinx, so it was
time for me to learn to use
[Sphinx](https://pypi.org/project/Sphinx/) and
[readthedocs](https://docs.readthedocs.io/en/stable/). For more
motivation, see this [Eric Holscher blog
post](https://www.ericholscher.com/blog/2016/mar/15/dont-use-markdown-for-technical-docs/).

## Setup documentation with Sphinx

The Getting Started guide on readthedocs starts with an
introduction to making documentation with Sphinx.

Install Sphinx:

```bash
$ pip install sphinx
```

Pick a project to document. Create a `docs` folder in the top level of the project repository:

```bash
$ mkdir docs
```

Setup documentation with `sphinx-quickstart`:

```bash
$ cd docs
$ sphinx-quickstart # launch cmdline UI for basic config
$ vim index.rst # edit project info
```

- `index.rst` is *reStructuredText*

## reST syntax:

- see reST syntax guide here:
  <https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html>

TLDR for Markdown users learning reST:

### lists

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

### italics, bold, monospace

```rst
*inline italics*
**inline bold**
``inline code``
```

## View documentation as HTML

Build the documentation:

```bash
$ make html
```

View the documentation by opening `_build/html/index.html` in a
web browser.

## Pick a better HTML theme

Open `docs/conf.py` and search for `html_theme`.

The default `html_theme` is *alabaster*:

```python
html_theme = "alabaster"
```

There are [a few built-in
themes](https://www.sphinx-doc.org/en/master/usage/theming.html).
For example, the official Python docs use *classic*.

Readthedocs offers its own theme:

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

## Use Markdown and reST in the same project

Install package `recommonmark` to use *Markdown* and *reST*
in the same Sphinx documentation build:

```bash
$ pip install recommonmark
```

Add `recommonmark` to the list of `extensions` in `conf.py`:

```python
extensions = ['recommonmark']
```

*Markdown* is easier to read but *reST* is more powerful. Use
*reST* for technical documentation:

<https://www.ericholscher.com/blog/2016/mar/15/dont-use-markdown-for-technical-docs/>

## Publish to readthedocs

Create an account on readthedocs and link it to your GitHub
account.

Import the GitHub repository into readthedocs and Build.

Sphinx documentation generated with `sphinx-quickstart` needs
this line added to the `conf.py` file:

```python
master_doc = 'index'
```

This overrides the readthedocs expectation for a file named
`contents.rst`.

