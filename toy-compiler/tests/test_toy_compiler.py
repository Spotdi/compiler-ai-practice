from __future__ import annotations

import sys
import unittest
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_DIR))

from ir_generator import SemanticError  # noqa: E402
from toycc import compile_source  # noqa: E402


class ToyCompilerTests(unittest.TestCase):
    def test_constant_folding_and_dead_code_elimination(self) -> None:
        source = """
        let x = 1 + 2 * 3;
        let y = x + 4;
        let unused = 10 * 20;
        print(y);
        """

        _, raw_ir, optimized_ir = compile_source(source)

        self.assertIn("unused = t3", raw_ir)
        self.assertEqual(["print 11"], optimized_ir)

    def test_assignment_and_reuse(self) -> None:
        source = """
        let x = 5;
        x = x + 2;
        print(x);
        """

        _, _, optimized_ir = compile_source(source)

        self.assertEqual(["print 7"], optimized_ir)

    def test_use_before_declaration_is_rejected(self) -> None:
        source = "print(x);"

        with self.assertRaises(SemanticError):
            compile_source(source)


if __name__ == "__main__":
    unittest.main()

