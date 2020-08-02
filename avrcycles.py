#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""Calculate clock cycles from AVR disassembly output.

Description:
    Open a .avra to analyze and hit ;avrt.
    Total number of clock cycles and instructions are
    displayed on the Vim command line and are available for
    cut and paste in the clipboard register.

    This script contains other potentially useful functions
    too, such as cleaning the .avra of all non-assembly
    code, or stripping the address and hex fields from the
    lines of assembly instructions.

    See also: avrasm.py

Usage:
    Output a .avra with avr-objdump.
    Example:
    $ avr-objdump -h -S build/vis-spi-out.elf > build/vis-spi-out.avra

    Grab a snippet to parse and put it in a new
    file. Run this script on the snippet.
    Example:
    $ avrcycles build/some-asm-snippet.avra

    This script prints the number of cycles total
    for the snippet.

    Invoke from Vim with ;avr. The output prints
    at the Vim command line. Vimscript that does
    this:

    ```vim
    execute "silent !$avrcycles % 2>&1 | clip"
    execute "normal! \<C-L>"
    redraw | echomsg s:happy_kitty "`".@+."`"
    ```

    .avra file path is the only command line argument.
    Run from Vim with shortcut `;avr`.
    Shortcut uses `%` at Vim command line for file in active buffer.

About:
    Calculating clock cycles by hand sucks.
"""

import argparse
from pathlib import Path

# Create a dictionary of AVR instructions to look
# up the number of clock cycles an instruction
# takes. Some instructions take more cycles under
# some condition. Return the maximum number of
# cycles in this case.
cycles={}
# Bit and bit-test instructions
cycles['sbi']=2
cycles['cbi']=2
cycles['cli']=1
cycles['sei']=1
# Arithmetic and logic instructions
cycles['com']=1 # one's complement
cycles['dec']=1 # decrement
cycles['and']=1
cycles['andi']=1
cycles['or']=1
cycles['add']=1
cycles['adc']=1
cycles['adiw']=2 # add immediate to word
cycles['sub']=1  # subtract two registers
cycles['subi']=1 # subtract constant from register
cycles['sbci']=1 # subtract with carry constant from register
cycles['sbiw']=2 # subtract immediate from word
cycles['eor']=1
cycles['ori']=1
# Data transfer instructions
cycles['in']=1 # in port
cycles['out']=1 # out port
cycles['ldi']=1
cycles['push']=2
cycles['pop']=2
cycles['mov']=1  # move between registers
cycles['movw']=1 # copy register word
cycles['lpm']=3  # load program memory
cycles['lds']=2  # load direct from SRAM
cycles['sts']=2  # store direct to SRAM
cycles['ldd']=2  # load indirect with displacement
cycles['std']=2  # store indirect with displacement
cycles['ld']=2   # load indirect
cycles['st']=2   # store indirect
# Branch instructions
cycles['sbis'] = 3 # skip if bit in I/O reg is set
# sbis: Datasheet lists #clocks=1/2/3, not sure what that means
cycles['sbic'] = 3 # skip if bit in I/O reg is cleared
# sbic: Datasheet lists #clocks=1/2/3, not sure what that means
cycles['sbrs'] = 3 # skip if bit in register is set
# sbrs: Datasheet lists #clocks=1/2/3, not sure what that means
cycles['cpi']=1  # compare register with immediate
cycles['cpc']=1  # compare with carry
cycles['cp']=1   # compare
cycles['cpse']=3 # compare, skip if equal
# cpse: Datasheet lists #clocks=1/2/3, not sure what that means
cycles['brpl']=2 # branch if plus (plus: SREG [N]eg Flag == 0)
# brpl: Datasheet lists #clocks=1/2, not sure what that means
cycles['rjmp']=2
cycles['jmp']=3
cycles['brne']=2
cycles['breq']=2
cycles['brcs']=2 # branch if carry set
cycles['brcc']=2 # branch if carry cleared
cycles['call']=4 # direct subroutine call
cycles['ret']=4
cycles['reti']=4

def print_every_line(fobj):
    """Print every line in the file.
    Report number of lines.
    """
    lines=[line for line in fobj]
    [print(line,end='') for line in lines]
    print(f"Total lines in file: {len(lines)}")
def _is_not_blank(line):
    """Return true if `line` is not blank."""
    return len(line.split())>0
def _is_blank(line):
    """Return true if `line` is blank."""
    return len(line.split())==0
def print_every_line_except_blanks(fobj):
    """Print every line in the file, but skip
    blank lines.
    Report number of lines.
    """
    # lines=[line.split() for line in fobj if len(line.split())>0]
    lines=[line.split() for line in fobj if _is_not_blank(line)]
    [print(line) for line in lines]
    print(
        "Total number of lines in file, "
        "skipping blank lines: "
        f"{len(lines)}"
        )
def _is_asm(line):
    """Return true if input `line` is a line of
    AVR assembly code.
    Identify AVR assembly lines by the first word.
    The first word is an address followed by a
    colon.
    Also check that the line contains at least
    three words: address, hex, and instruction
    Example:
        ' 1b6:	ff cf 	rjmp	.-2  	;'
    """
    # Discard blank lines
    if _is_blank(line):
        return False
    # Check first word
    word1=line.split()[0]
    word1_last_char=word1[-1]
    line_has_at_least_3_words=len(line.split())>2
    return (
        word1[0:-1].isalnum()
        and word1_last_char is ':'
        and line_has_at_least_3_words
        )
def print_only_asm_lines(fobj):
    """Print only assembly lines of code from the
    file.
    Report number of lines.
    """
    lines=[line for line in fobj if _is_asm(line)]
    [print(line.split('\t')) for line in lines]
    print(
        "Total number of assembly lines in file: "
        f"{len(lines)}"
        )
def _instruction(asm_line):
    """Return the instruction found in input
    `asm_line`, a line of AVR Assembly code.
    Example:
        ' 1b6:	ff cf 	rjmp	.-2  	;'
    Returns the string: "rjmp"
    """
    # Lines are tab-separated.
    # Instruction is always the 3rd word.
    return asm_line.split('\t')[2].strip()
def list_of_instructions_in_file(fobj):
    """Return a list of assembly instructions parsed from
    the input `fobj` file object. Duplicates are included.
    The length of the final list equals the number of lines
    of assembly code in the file.
    Find a line of assembly.
    Extract the instruction.
    Append it to the list.
    """
    # Get all the assembly lines
    lines=[line for line in fobj if _is_asm(line)]
    # return the list of instructions
    return [_instruction(line) for line in lines]
def print_instruction_from_every_line(fobj):
    """Print the instructions from an AVR Assembly
    file. Ignore lines that are not AVR Assembly.
    """
    # Get all the assembly lines
    # lines=[line for line in fobj if _is_asm(line)]
    # Pull out the instructions
    # instructions=[_instruction(line) for line in lines]
    instructions=list_of_instructions_in_file(fobj)
    [print(inst,end=', ') for inst in instructions]
    print(
        "\nTotal number of assembly instructions: "
        f"{len(instructions)}"
        )
def Parse_avra(filepath):
    """Docstring
    """
    # Open file
    p = Path(filepath)
    with p.open() as f:
        # print_every_line(f)
        # print_every_line_except_blanks(f)
        # print_only_asm_lines(f)
        # print_instruction_from_every_line(f)
        # Find each AVR instruction
        instructions=list_of_instructions_in_file(f)
        # Look up the number of cycles for that instruction
        cycles_list=[cycles[instr] for instr in instructions]
        # Total the number of cycles.
        print(f"Total number of cycles: {sum(cycles_list)}")
        print(f"Total number of instructions: {len(instructions)}")

if __name__ == '__main__':
    # Take the file path as a command line argument.

    # Create a parser.
    parser = argparse.ArgumentParser()

    # Add a positional arg.
    parser.add_argument(
        'avra',
        metavar='Path-to-AVRA-file',
        type=str,
        help='Path to .avra file.'
        )

    # =====[ the critical LOC to make this a utility. ]=====
    # Parse space-separated text after `pkgscripts`.
    args = parser.parse_args()

    # Validate the *avra file path* argument.
    path = Path(args.avra)
    # Stop execution if the file is not found.
    assert path.exists(), f'\n  File "{path.name}" not found. Check your path:\n"{path}"'
    # Stop execution if the path is not a file.
    assert path.is_file(), f'\n  Path is not a file:\n "{path}"'
    # Stop execution if the path is not an avra.
    assert path.suffix == '.avra', f'\n  File type "{path.suffix}" is not .avra!'

    Parse_avra(filepath=path)
