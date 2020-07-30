I really just created this repository to learn how to setup
documentation on readthedocs:
<https://docs.readthedocs.io/en/stable/>.

The *project* is just one Python script: `avrcycles.py`. This was
a quick-fix at work: I was analyzing disassembly to compare
execution time with and without interrupts. I got tired of
looking up how long each instruction was and manually adding the
cycle times.

`avrcycles.py` started out as a dictionary of cycle times for the
code in question and a parser to pull the instruction from each
line of code.

I add to the dictionary as I analyze new assembly code and
encounter instructions I did not include yet. I still don't have
*all* the instructions in here, but I've run this script on *a
lot* of assembly code and have not run into any missing
instructions yet.
