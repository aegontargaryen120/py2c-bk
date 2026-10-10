import tempfile
import unittest
from pathlib import Path

from py2c import CProgram, CReturn, CRawStatement


class TestCProgram(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.output = Path(self.temp_dir.name) / "output.c"
        self.program = CProgram(str(self.output))

    def test_system_include(self):
        self.program.include_("stdio.h")

        self.assertEqual(
            self.program.render_(),
            "#include <stdio.h>\n\n",
        )

    def test_local_include(self):
        self.program.include_("my_header.h", system=False)

        self.assertEqual(
            self.program.render_(),
            '#include "my_header.h"\n\n',
        )

    def test_duplicate_include_exits(self):
        self.program.include_("stdio.h")

        with self.assertRaises(SystemExit):
            self.program.include_("stdio.h")

    def test_function_definition(self):
        self.program.defun_("main", "int", ["void"])

        self.assertEqual(
            self.program.render_(),
            "int main(void) {\n}\n\n",
        )

    def test_function_parameters(self):
        self.program.defun_(
            "add",
            "int",
            ["int a", "int b"],
        )

        self.assertEqual(
            self.program.render_(),
            "int add(int a, int b) {\n}\n\n",
        )

    def test_add_creates_raw_statement(self):
        function = self.program.defun_("main", "int", ["void"])
        function.add("int x = 42")

        self.assertEqual(
            function.body,
            [CRawStatement("int x = 42;")],
        )

    def test_return_creates_return_statement(self):
        function = self.program.defun_("main", "int", ["void"])
        function.return_("0")

        self.assertEqual(
            function.body,
            [CReturn("0;")],
        )

    def test_statement_rendering(self):
        function = self.program.defun_("main", "int", ["void"])
        function.add('printf("Hello, world!")')
        function.return_("0")

        self.assertEqual(
            self.program.render_(),
            'int main(void) {\n'
            '  printf("Hello, world!");\n'
            '  return 0;\n'
            '}\n\n',
        )

    def test_multiple_functions_preserve_order(self):
        self.program.defun_("first", "void", [])
        self.program.defun_("second", "void", [])

        source = self.program.render_()

        self.assertLess(
            source.index("first()"),
            source.index("second()"),
        )

    def test_empty_program(self):
        self.assertEqual(self.program.render_(), "")

    def test_generate_writes_source(self):
        self.program.include_("stdio.h")
        function = self.program.defun_("main", "int", ["void"])
        function.return_("0")

        expected = self.program.render_()
        self.program.generate_()

        self.assertTrue(self.output.exists())
        self.assertEqual(
            self.output.read_text(encoding="utf-8"),
            expected,
        )


if __name__ == "__main__":
    unittest.main()

