.. This is the README on the GitHub homepage.

avrcycles
=========

The *project* is just one Python script: ``avrcycles.py``.

``avrcycles.py`` reports how many clock cycles are consumed:

* pull the assembly instruction pneumonic from each line of code
  in the ``.avra`` file to analyze
* look up each instruction in a dictionary to find the number of
  cycles consumed by that instruction
* report the total number of cycles consumed by the code in the
  ``.avra`` file

Usage
*****

* manually identify a block of assembly that corresponds to the C code in
  question
* paste this block into a new ``.avra`` file
* run ``avrcycles.py`` on that file

**Example**:

::

    avrcycles.py temp.avra

Documentation
*************

See more documentation on [readthedocs](https://avrcycles.readthedocs.io/en/latest/).
