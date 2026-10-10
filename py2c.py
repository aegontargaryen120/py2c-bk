from __future__ import annotations
from dataclasses import dataclass, field
import sys

@dataclass
class CFunction:
    name: str
    return_type: str
    params: list[str]
    body: list[CStatement] = field(default_factory=list)

    def add(self, source: str) -> None:
        self.body.append(CRawStatement(source + ";"))


    def return_(self, return_value: str) -> None:
        self.body.append(CReturn(return_value + ";"))


@dataclass
class Include:
    name: str
    system: bool


@dataclass
class CStatement:
    pass


@dataclass
class CRawStatement(CStatement):
    source: str


@dataclass
class CReturn(CStatement):
    expression: str


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


    def render_(self) -> str:
        rendered_source = ""

        if self.includes:
            for include in self.includes:
                if include.system:
                    rendered_source += f"#include <{include.name}>\n"
                else:
                    rendered_source += f'#include "{include.name}"\n'
            rendered_source += "\n"

        for function in self.functions:
            if len(function.params) == 1:
                params = function.params[0]
            elif len(function.params) > 1:
                params = ", ".join(function.params)
            else:
                params = "void"

            rendered_source += f"{function.return_type} {function.name}({params}) {{\n"

            for stmt in function.body:
                if isinstance(stmt, CRawStatement):
                    rendered_source += "  " + stmt.source + "\n"
                elif isinstance(stmt, CReturn):
                    rendered_source += "  return " + stmt.expression + "\n"
                else:
                    print("\033[1;31mERROR:\033[0m statement not identified, in `CProgram.render_()`")

            rendered_source += "}\n\n"

        return rendered_source


    def generate_(self) -> None:
        with open(self.file_name, 'w') as out:
            out.write(self.render_())
