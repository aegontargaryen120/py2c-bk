from dataclasses import dataclass, field
import sys

@dataclass
class CFunction:
    name: str
    return_type: str
    params: list[str]
    body: list[str] = field(default_factory=list)


@dataclass
class Include:
    name: str
    system: bool


class CProgram:
    def __init__(self, file_name: str) -> None:
        self.file_name = file_name
        self.includes: list[Include] = []
        self.functions: list[CFunction] = []

    def include_(self, header: str, system: bool = True) -> None:
        new_include = Include(header, system)
        if new_include not in self.includes:
            self.includes.append(new_include)
        else:
            print(f"\033[1;31mERROR:\033[0m header file `{header}` already included.")
            sys.exit(1)

    def defun_(self, name: str, return_type: str, params: list[str]) -> CFunction:
        fn = CFunction(name, return_type, params)
        self.functions.append(fn)
        return fn

    def generate_(self) -> None:
        with open(self.file_name, 'w') as out:
            if self.includes:
                for include in self.includes:
                    if include.system:
                        out.write(f"#include <{include.name}>\n")
                    else:
                        out.write(f'#include "{include.name}"\n')
                out.write("\n")

            for function in self.functions:
                param_str = ", ".join(function.params)
                out.write(f"{function.return_type} {function.name}({param_str}) {{\n")
                
                for line in function.body:
                    out.write(f"    {line}\n")
                
                out.write("}\n\n")

