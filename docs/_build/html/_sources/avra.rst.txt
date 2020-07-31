AVRA
====

AVRA -- assembler for the Atmel AVR microcontrollers

AVRA project homepage: https://github.com/Ro5bert/avra

Here is my ``make`` recipe using ``avr-objdump`` to generate a
``.avra`` file from the ``.elf`` file:

.. code-block:: make

   build/%.avra: build/%.elf
       avr-objdump -h -S $^ > $@

* ``-h``: list space used by each section
* ``-S``: output the binary (assembly code) with source code
  (C code)

.. note::
   I name this file with extension `.avra` solely to pick up the
   correct syntax highlighting in Vim. I'm not sure this file is
   actually any different from the AVRASM32 file as distinguised
   on the AVRA project homepage.

   Other assembly file extensions are ``.lst`` and ``.asm``.
   Again, I'm just using ``.avra`` for the syntax
   highlighting in my code editor.


