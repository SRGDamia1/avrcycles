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
cycles = {
    "adc": 1,
    "add": 1,
    "adiw": 2,
    "and": 1,
    "andi": 1,
    "asr": 1,
    "bclr": 1,
    "bld": 1,
    "brbc": 2,
    "brbs": 2,
    "brcc": 2,
    "brcs": 2,
    "break": 1,
    "breq": 2,
    "brge": 2,
    "brhc": 2,
    "brhs": 2,
    "brid": 2,
    "brie": 2,
    "brlo": 2,
    "brlt": 2,
    "brmi": 2,
    "brne": 2,
    "brpl": 2,
    "brsh": 2,
    "brtc": 2,
    "brts": 2,
    "brvc": 2,
    "brvs": 2,
    "bset": 2,
    "bst": 2,
    "call": 5,
    "cbi": 2,
    "cbr": 3,
    "clc": 3,
    "clh": 1,
    "cli": 1,
    "cln": 6,
    "clr": 6,
    "cls": 2,
    "clt": 1,
    "clv": 1,
    "clz": 1,
    "com": 2,
    "cp": 2,
    "cpc": 2,
    "cpi": 2,
    "cpse": 3,
    "dec": 2,
    "des": 2,
    "eicall": 4,
    "eijmp": 2,
    "elpm": 3,
    "elpm": 3,
    "elpm": 3,
    "eor": 1,
    "fmul": 2,
    "fmuls": 2,
    "fmulsu": 2,
    "icall": 4,
    "ijmp": 2,
    "in": 1,
    "inc": 1,
    "jmp": 3,
    "lac": 2,
    "las": 2,
    "lat": 2,
    "ld": 2,
    "ld": 2,
    "ld": 2,
    "ld": 2,
    "ld": 2,
    "ld": 3,
    "ld": 3,
    "ld": 2,
    "ld": 3,
    "ldd": 3,
    "ldd": 3,
    "ldi": 2,
    "lds": 3,
    "lpm": 3,
    "lpm": 3,
    "lpm": 3,
    "lsl": 1,
    "lsr": 1,
    "mov": 2,
    "movw": 1,
    "mul": 2,
    "muls": 2,
    "mulsu": 2,
    "neg": 1,
    "nop": 1,
    "or": 1,
    "ori": 1,
    "out": 1,
    "pop": 2,
    "push": 2,
    "rcall": 4,
    "ret": 5,
    "reti": 5,
    "rjmp": 2,
    "rol": 1,
    "ror": 1,
    "sbc": 1,
    "sbci": 1,
    "sbi": 3,
    "sbic": 4,
    "sbis": 4,
    "sbiw": 2,
    "sbr": 1,
    "sbrc": 3,
    "sbrs": 3,
    "sec": 1,
    "seh": 1,
    "sei": 1,
    "sen": 1,
    "ser": 1,
    "ses": 1,
    "set": 1,
    "sev": 1,
    "sez": 1,
    "sleep": 1,
    "spm": 4,
    "spm": 4,
    "st": 2,
    "st": 2,
    "st": 2,
    "st": 2,
    "st": 2,
    "st": 2,
    "st": 2,
    "st": 2,
    "st": 2,
    "std": 2,
    "std": 2,
    "sts": 2,
    "sub": 1,
    "subi": 1,
    "swap": 1,
    "tst": 1,
    "wdr": 1,
    "xch": 2,
}


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
