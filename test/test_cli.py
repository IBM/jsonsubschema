"""
Test suite for CLI interface.

This module tests the command-line interface for jsonsubschema including:
- Basic CLI invocation
- File loading
- Error handling
- Output formatting

Created to ensure CLI interface works correctly.
"""

import json
import os
import subprocess
import tempfile
import unittest


class TestCLIBasicUsage(unittest.TestCase):
    """Test basic CLI functionality."""

    def setUp(self):
        """Create temporary test files."""
        self.temp_dir = tempfile.mkdtemp()
        self.s1_path = os.path.join(self.temp_dir, "s1.json")
        self.s2_path = os.path.join(self.temp_dir, "s2.json")

    def tearDown(self):
        """Clean up temporary files."""
        if os.path.exists(self.s1_path):
            os.remove(self.s1_path)
        if os.path.exists(self.s2_path):
            os.remove(self.s2_path)
        if os.path.exists(self.temp_dir):
            os.rmdir(self.temp_dir)

    def _write_schema(self, path, schema):
        """Helper to write schema to file."""
        with open(path, "w") as f:
            json.dump(schema, f)

    def _run_cli(self, lhs_path, rhs_path):
        """Helper to run CLI and capture output."""
        result = subprocess.run(
            ["python", "-m", "jsonsubschema.cli", lhs_path, rhs_path],
            capture_output=True,
            text=True,
        )
        return result

    def test_cli_basic_true(self):
        """Test CLI with subtype relationship (returns True)."""
        s1 = {"type": "integer"}
        s2 = {"type": ["integer", "string"]}
        self._write_schema(self.s1_path, s1)
        self._write_schema(self.s2_path, s2)

        result = self._run_cli(self.s1_path, self.s2_path)
        self.assertEqual(result.returncode, 0)
        self.assertIn("True", result.stdout)

    def test_cli_basic_false(self):
        """Test CLI with non-subtype relationship (returns False)."""
        s1 = {"type": "string"}
        s2 = {"type": "integer"}
        self._write_schema(self.s1_path, s1)
        self._write_schema(self.s2_path, s2)

        result = self._run_cli(self.s1_path, self.s2_path)
        self.assertEqual(result.returncode, 0)
        self.assertIn("False", result.stdout)

    def test_cli_empty_schemas(self):
        """Test CLI with empty schemas."""
        s1 = {}
        s2 = {}
        self._write_schema(self.s1_path, s1)
        self._write_schema(self.s2_path, s2)

        result = self._run_cli(self.s1_path, self.s2_path)
        self.assertEqual(result.returncode, 0)
        self.assertIn("True", result.stdout)

    def test_cli_complex_schemas(self):
        """Test CLI with complex schemas."""
        s1 = {
            "type": "object",
            "properties": {"name": {"type": "string"}, "age": {"type": "integer"}},
            "required": ["name", "age"],
        }
        s2 = {
            "type": "object",
            "properties": {"name": {"type": "string"}},
            "required": ["name"],
        }
        self._write_schema(self.s1_path, s1)
        self._write_schema(self.s2_path, s2)

        result = self._run_cli(self.s1_path, self.s2_path)
        self.assertEqual(result.returncode, 0)
        self.assertIn("True", result.stdout)


class TestCLIFileHandling(unittest.TestCase):
    """Test CLI file handling."""

    def setUp(self):
        """Create temporary test directory."""
        self.temp_dir = tempfile.mkdtemp()
        self.valid_path = os.path.join(self.temp_dir, "valid.json")

    def tearDown(self):
        """Clean up temporary files."""
        if os.path.exists(self.valid_path):
            os.remove(self.valid_path)
        if os.path.exists(self.temp_dir):
            os.rmdir(self.temp_dir)

    def _write_schema(self, path, schema):
        """Helper to write schema to file."""
        with open(path, "w") as f:
            json.dump(schema, f)

    def _run_cli(self, lhs_path, rhs_path):
        """Helper to run CLI and capture output."""
        result = subprocess.run(
            ["python", "-m", "jsonsubschema.cli", lhs_path, rhs_path],
            capture_output=True,
            text=True,
        )
        return result

    def test_cli_missing_lhs_file(self):
        """Test CLI with missing LHS file."""
        self._write_schema(self.valid_path, {"type": "string"})
        nonexistent = os.path.join(self.temp_dir, "nonexistent.json")

        result = self._run_cli(nonexistent, self.valid_path)
        self.assertNotEqual(result.returncode, 0)

    def test_cli_missing_rhs_file(self):
        """Test CLI with missing RHS file."""
        self._write_schema(self.valid_path, {"type": "string"})
        nonexistent = os.path.join(self.temp_dir, "nonexistent.json")

        result = self._run_cli(self.valid_path, nonexistent)
        self.assertNotEqual(result.returncode, 0)

    def test_cli_invalid_json_lhs(self):
        """Test CLI with invalid JSON in LHS file."""
        invalid_path = os.path.join(self.temp_dir, "invalid.json")
        with open(invalid_path, "w") as f:
            f.write("{invalid json")

        self._write_schema(self.valid_path, {"type": "string"})

        result = self._run_cli(invalid_path, self.valid_path)
        self.assertNotEqual(result.returncode, 0)

        os.remove(invalid_path)

    def test_cli_invalid_json_rhs(self):
        """Test CLI with invalid JSON in RHS file."""
        invalid_path = os.path.join(self.temp_dir, "invalid.json")
        with open(invalid_path, "w") as f:
            f.write("{invalid json")

        self._write_schema(self.valid_path, {"type": "string"})

        result = self._run_cli(self.valid_path, invalid_path)
        self.assertNotEqual(result.returncode, 0)

        os.remove(invalid_path)


class TestCLIArguments(unittest.TestCase):
    """Test CLI argument handling."""

    def _run_cli(self, args):
        """Helper to run CLI with specific arguments."""
        result = subprocess.run(
            ["python", "-m", "jsonsubschema.cli"] + args,
            capture_output=True,
            text=True,
        )
        return result

    def test_cli_no_arguments(self):
        """Test CLI with no arguments."""
        result = self._run_cli([])
        self.assertNotEqual(result.returncode, 0)
        self.assertTrue(len(result.stderr) > 0)

    def test_cli_one_argument(self):
        """Test CLI with only one argument."""
        result = self._run_cli(["schema1.json"])
        self.assertNotEqual(result.returncode, 0)
        self.assertTrue(len(result.stderr) > 0)

    def test_cli_help_flag(self):
        """Test CLI with help flag."""
        result = self._run_cli(["--help"])
        self.assertEqual(result.returncode, 0)
        self.assertIn("usage", result.stdout.lower())


if __name__ == "__main__":
    unittest.main()
