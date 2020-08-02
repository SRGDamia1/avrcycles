.. This is the README on the GitHub homepage.

avrcycles
=========

The *project* is just one Python script: ``avrcycles.py``.

``avrcycles.py`` was a quick-fix at work: I was analyzing
disassembly to compare execution time with and without
interrupts. I got tired of manually looking up the cycles times
for each instruction and adding them together.

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

Example:

::

    avrcycles.py temp.avra

Instruction Set Dictionary
**************************

I couldn't find the instructions summary in plain text or csv
form on the internet, so I manually copied the dictionary of
instructions in ``avrcycles.py`` from the *Instruction Set
Summary* at the end of the ATmega328P datasheet PDF. I didn't
copy all the instructions, just the ones I needed. I only add to
the list when I get an error that the dictionary is missing an
instruction used in the ``.avra`` file.
