# Py2C&Bk version 1

## Description:
> Added a simple script that uses string manipulation and file writing to build out a script in C, generated entirely from function calls. 
---

## API:
* Class `CProgram`. Use: `file = CProgram("file_name.c")`
* Function `CProgram.include_`. Use: `file.include_("stdio.h", system=True)`
* Function `CProgram.defun_`. Use: `function = file.defun_("main", "int", ["int argc", "char **argv"])`
* Function `CProgram.generate_`. Use: `file.generate()`

### Class `CProgram`
This is the base class for a C file. It takes in a name in the constructor, and includes a list of functions that can help you write a C file.
### Function `CProgram.include_`
This is the function for including headers in a C file. It takes in a parameter name, and an optional boolean value of `system` for switching between `#include <stdio.h>` and `#include "common.h"`
### Function `CProgram.defun_`
This creates a new `CFunction` class and puts it in the program. It takes in a name, return type, and parameters. You can append strings to the function as a "body", which will be generated when the `CProgram.generate_` is called.
### Function `CProgram.generate_`
This function generates the C code and writes it to the file.

