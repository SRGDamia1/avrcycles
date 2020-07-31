Usage
=====

 .. code-block:: bash

    avrcycles.py temp.avra

Example output:

 .. code-block:: md

    Total number of cycles: 6
    Total number of instructions: 4

Detailed Usage
==============

* generate disassembly from the ``.elf`` file

    .. code-block:: bash

       avr-objdump -h -S board.elf > board.avra

    * ``-h``: list space used by each section
    * ``-S``: output the binary (assembly code) with source code
      (C code)

* paste the snippet of assembly to analyze into a file

    * example assembly snippet:

    .. code-block::
       :emphasize-lines: 3-6

       // Initialize exposure time to 1 millisecond
       exposure_ticks = 50; // 50 ticks = (1.0e-3 s)/(20.0e-6 s/tick)
        1c0:	82 e3       	ldi	r24, 0x32	; 50
        1c2:	90 e0       	ldi	r25, 0x00	; 0
        1c4:	90 93 1d 01 	sts	0x011D, r25	; 0x80011d <exposure_ticks+0x1>
        1c8:	80 93 1c 01 	sts	0x011C, r24	; 0x80011c <exposure_ticks>

    .. note::
        I usually call this snippet file ``temp.avra`` so I
        know it's safe to delete later

    * in the above example, only the four high-lighted lines of
      code are analyzed

        * the parser in ``avrcycles.py`` ignores the first two
          lines vebecause they are not assembly
        * non-assembly lines are included in the .avra because of
          the ``-S`` flag

* run ``avrcycles.py`` from the command line (e.g., from bash)

     .. code-block:: bash

        avrcycles.py temp.avra

* example output:

     .. code-block:: md

        Total number of cycles: 6
        Total number of instructions: 4


