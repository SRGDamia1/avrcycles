How avrcycles works
===================

* ``avrcycles.py`` uses a Python dictionary of AVR instructions

    * :key: instruction pneumonic (example: ``SBI`` -- *Set Bit
            in I/O Register*)
    * :value: number of clock cycles (example: ``2``)

        * for instructions with variable numbers of cycles, I use
          the maximum number of cycles listed in the datasheet
        * **example**:

            * instruction ``SBRC`` (*Skip if Bit in Register is
              Set*) lists ``#Clocks`` as ``1/2/3``
            * so I use **3 cycles** in my dictionary

* parse the ``.avra`` file (the disassembly output):

    * for each line of assembly
    * extract the instruction
    * append it to a list of instructions

* use the dictionary to look up the number of clock cycles for each instruction
  in the list

    * for each instruction in the list
    * look up the number of cycles
    * append it to a list of cycles

* sum the list of cycles to calculate the total number of cycles consumed by the
  assembly code listed in the ``.avra`` file
