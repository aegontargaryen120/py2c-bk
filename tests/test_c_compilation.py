
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from py2c import CProgram


class TestCCompilation(unittest.TestCase):
    def test_generated_program_compiles_and_runs(self):
        compiler = (
            shutil.which("cc")
            or shutil.which("clang")
            or shutil.which("gcc")
        )

        if compiler is None:
            self.skipTest("No C compiler installed")

        with tempfile.TemporaryDirectory() as temp_dir:
            source_file = Path(temp_dir) / "hello.c"
            executable = Path(temp_dir) / "hello"

            program = CProgram(str(source_file))
            program.include_("stdio.h")

            main = program.defun_("main", "int", ["void"])
            main.add('printf("Hello from Py2C!\\n")')
            main.return_("0")

            program.generate_()

            compilation = subprocess.run(
                [compiler, str(source_file), "-o", str(executable)],
                capture_output=True,
                text=True,
            )

            self.assertEqual(
                compilation.returncode,
                0,
                compilation.stderr,
            )

            execution = subprocess.run(
                [str(executable)],
                capture_output=True,
                text=True,
            )

            self.assertEqual(execution.returncode, 0)
            self.assertEqual(execution.stdout, "Hello from Py2C!\n")


if __name__ == "__main__":
    unittest.main()

