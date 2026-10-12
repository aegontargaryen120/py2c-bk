# Py2C&Bk version 1

## Description:
> Added a way to directly write content to a file instead of having it in a function.

---

## API:
* Class `CProgram`. Use: `file = CProgram("file_name.c")`
* Function `CProgram.include_`. Use: `file.include_("stdio.h", system=True)`
* Function `CProgram.defun_`. Use: `function = file.defun_("main", "int", ["int argc", "char **argv"])`
* Function `CProgram.generate_`. Use: `file.generate_()`
* Function `CProgram.render_`. Use: `print(file.render_())`
* Function `CFunction.add`. Use: `function.add('printf("Hello!\n")')`
* Function `CFunction.return_`. Use: `function.return_("0")`
* Function `CProgram.add_`. Use: `file.add("this is my source")`

### Class `CProgram`
This is the base class for a C file. It takes in a name in the constructor, and includes a list of functions that can help you write a C file.
### Function `CProgram.include_`
This is the function for including headers in a C file. It takes in a parameter name, and an optional boolean value of `system` for switching between `#include <stdio.h>` and `#include "common.h"`
### Function `CProgram.defun_`
This creates a new `CFunction` class and puts it in the program. It takes in a name, return type, and parameters. You can append strings to the function as a "body", which will be generated when the `CProgram.generate_` is called.
### Function `CProgram.generate_`
This function writes the generated C code to the file.
### Function `CProgram.render_()`
This function generates and returns the generated C code. It is used in `generate_` to generate the code, before writing.
### Function `CFunction.add`
This function adds a string of C source to the function's body.
> **NOTE**: You do not need to terminate a string with `;` if you are using the `add` function, because the function adds that in for you
### Function `CFunction.return_`
This function takes in a value, e.g. `0` or `"Hello!"` and adds a return statement with that value to the program.
> **NOTE**: You do not need to terminate a string with `;` if you are using the `return_` function, because the function adds that in for you 
### Function `CProgram.add_`
This function takes in a string and adds it to the file, instead of needing to have it in a function.
> **NOTE**: You need to terminate the string passed to this function with a `;` because it does not automatically add that for you.

