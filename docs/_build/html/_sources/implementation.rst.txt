How avrcycles works
===================

``avrcycles.py`` was a quick-fix at work: I was analyzing
disassembly to compare execution time with and without
interrupts. I got tired of manually looking up the cycles times
for each instruction and adding them together.

Instruction Set Dictionary
**************************

I couldn't find the instructions summary in plain text or csv
form on the internet, so I manually copied the dictionary of
instructions in ``avrcycles.py`` from the *Instruction Set
Summary* at the end of the ATmega328P datasheet PDF. I didn't
copy all the instructions, just the ones I needed. I only add to
the list when I get an error that the dictionary is missing an
instruction used in the ``.avra`` file.

Use a dictionary
****************

``avrcycles.py`` uses a Python dictionary of AVR instructions:

    * :key: instruction pneumonic
    * :value: number of clock cycles

**Example**:

* *Set Bit in I/O Register*:

    * **pneumonic**: ``SBI``
    * **clock cycles**: ``2``

 .. code-block:: python

    cycles['sbi'] = 2

For instructions with variable numbers of cycles, I use the
maximum number of cycles listed in the datasheet.

**Example**:

* instruction ``SBRS`` (*Skip if Bit in Register is
  Set*) lists ``#Clocks`` as ``1/2/3``
* so I use **3 cycles** in my dictionary

.. code-block:: python

    cycles['sbrs'] = 3

Parse assembly code
*******************

Parse the ``.avra`` file (the disassembly output):

* for each line of assembly
* extract the instruction
* append it to a list of instructions

Dictionary look up
******************

Use the dictionary to look up the number of clock cycles for each
instruction in the list:

* for each instruction in the list
* look up the number of cycles
* append it to a list of cycles

Report total
************

Sum the list of cycles to calculate the total number of cycles
consumed by the assembly code listed in the ``.avra`` file.
