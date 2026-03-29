from __future__ import print_function

import argparse
import subprocess
import sys
import unittest
from unittest.mock import patch

PYTHON = sys.executable

MODULES = {
    "mutate": "universalmutator.genmutants",
    "analyze_mutants": "universalmutator.analyze",
    "check_covered": "universalmutator.checkcov",
    "find_missing": "universalmutator.findmissing",
    "intersect_mutants": "universalmutator.intersect",
    "prioritize_mutants":"universalmutator.prioritize",
    "prune_mutants": "universalmutator.prune",
    "show_mutants": "universalmutator.show",
}

# UNIT TESTING ALL ARGS ADDED BY 3/28/2026 (any args added after that date have not been included)


def run_module(module, args):
    return subprocess.run(
        [PYTHON, "-m", module] + args,
        capture_output=True, text=True
    )


def capture_parsed_args(module_main, argv):

    captured = {}
    original_parse_args = argparse.ArgumentParser.parse_args

    def intercepting(self, args=None, namespace=None):
        result = original_parse_args(self, args, namespace)
        captured["parsed"] = result
        return result

    with patch.object(argparse.ArgumentParser, "parse_args", intercepting):
        with patch("sys.argv", argv):
            try:
                module_main()
            except (SystemExit, Exception):
                pass

    return captured.get("parsed")


# 1. --help exits 0 for every command

class TestHelpOutput(unittest.TestCase):

    def _check_help(self, module):
        result = run_module(module, ["--help"])
        self.assertEqual(result.returncode, 0,
                         msg=f"{module} --help returned {result.returncode}\n{result.stderr}")
        self.assertIn("usage", result.stdout.lower())

    def test_mutate_help(self): self._check_help(MODULES["mutate"])
    def test_analyze_help(self): self._check_help(MODULES["analyze_mutants"])
    def test_check_covered_help(self): self._check_help(MODULES["check_covered"])
    def test_find_missing_help(self): self._check_help(MODULES["find_missing"])
    def test_intersect_mutants_help(self):self._check_help(MODULES["intersect_mutants"])
    def test_prioritize_mutants_help(self):self._check_help(MODULES["prioritize_mutants"])
    def test_prune_mutants_help(self): self._check_help(MODULES["prune_mutants"])
    def test_show_mutants_help(self): self._check_help(MODULES["show_mutants"])


# 2. Missing required positional args goes to exit code 2

class TestMissingRequiredArgs(unittest.TestCase):

    def _assert_usage_error(self, module, args):
        result = run_module(module, args)
        self.assertEqual(result.returncode, 2,
                         msg=f"Expected exit 2 for {module} {args}\n{result.stderr}")

    def test_mutate_requires_source(self):
        self._assert_usage_error(MODULES["mutate"], [])

    def test_analyze_requires_sourcefile(self):
        self._assert_usage_error(MODULES["analyze_mutants"], [])

    def test_analyze_requires_testscript(self):
        self._assert_usage_error(MODULES["analyze_mutants"], ["src.py"])

    def test_check_covered_requires_sourcefile(self):
        self._assert_usage_error(MODULES["check_covered"], [])

    def test_check_covered_requires_coverfile(self):
        self._assert_usage_error(MODULES["check_covered"], ["src.py"])

    def test_check_covered_requires_outfile(self):
        self._assert_usage_error(MODULES["check_covered"], ["src.py", "cover.txt"])

    def test_find_missing_requires_all_three(self):
        self._assert_usage_error(MODULES["find_missing"], [])
        self._assert_usage_error(MODULES["find_missing"], ["foo.py"])
        self._assert_usage_error(MODULES["find_missing"], ["foo.py", "dir1"])

    def test_intersect_requires_all_three(self):
        self._assert_usage_error(MODULES["intersect_mutants"], [])
        self._assert_usage_error(MODULES["intersect_mutants"], ["a.txt"])
        self._assert_usage_error(MODULES["intersect_mutants"], ["a.txt", "b.txt"])

    def test_prioritize_requires_infile_and_outfile(self):
        self._assert_usage_error(MODULES["prioritize_mutants"], [])
        self._assert_usage_error(MODULES["prioritize_mutants"], ["in.txt"])

    def test_prune_requires_all_three(self):
        self._assert_usage_error(MODULES["prune_mutants"], [])
        self._assert_usage_error(MODULES["prune_mutants"], ["in.txt"])
        self._assert_usage_error(MODULES["prune_mutants"], ["in.txt", "out.txt"])

    def test_show_requires_infile(self):
        self._assert_usage_error(MODULES["show_mutants"], [])


# 3. Type validation (argparse rejects bad types before touching files)

class TestTypeValidation(unittest.TestCase):

    def _assert_type_error(self, module, args):
        result = run_module(module, args)
        self.assertEqual(result.returncode, 2,
                         msg=f"Expected type error (exit 2) for {module} {args}\n{result.stderr}")

    def test_analyze_seed_must_be_int(self):
        self._assert_type_error(MODULES["analyze_mutants"],
                                ["src.py", "pytest", "--seed", "notanint"])

    def test_analyze_timeout_must_be_float(self):
        self._assert_type_error(MODULES["analyze_mutants"],
                                ["src.py", "pytest", "--timeout", "notafloat"])

    def test_analyze_num_mutants_must_be_int(self):
        self._assert_type_error(MODULES["analyze_mutants"],
                                ["src.py", "pytest", "--numMutants", "notanint"])

    def test_prioritize_cutoff_must_be_float(self):
        self._assert_type_error(MODULES["prioritize_mutants"],
                                ["in.txt", "out.txt", "--cutoff", "notafloat"])

    def test_prioritize_N_must_be_int(self):
        self._assert_type_error(MODULES["prioritize_mutants"],
                                ["in.txt", "out.txt", "notanint"])


# 4. Default values
class TestDefaults(unittest.TestCase):

    def test_mutate_defaults(self):
        from universalmutator.genmutants import main
        p = capture_parsed_args(main, ["mutate", "source.py"])
        self.assertIsNotNone(p)
        self.assertEqual(p.source, "source.py")
        self.assertIsNone(p.language_or_rules)
        self.assertEqual(p.rules, [])
        self.assertFalse(p.noCheck)
        self.assertFalse(p.comby)
        self.assertFalse(p.redundantOK)
        self.assertFalse(p.showRules)
        self.assertFalse(p.mutateInStrings)
        self.assertFalse(p.mutateTestCode)
        self.assertFalse(p.mutateBoth)
        self.assertFalse(p.noFastCheck)
        self.assertFalse(p.swap)
        self.assertFalse(p.tstl)
        self.assertFalse(p.fuzz)
        self.assertFalse(p.printStat)
        self.assertIsNone(p.cmd)
        self.assertIsNone(p.lines)
        self.assertEqual(p.mutantDir, ".")
        self.assertIsNone(p.ignore)
        self.assertIsNone(p.compile)
        self.assertIsNone(p.only)

    def test_analyze_defaults(self):
        from universalmutator.analyze import main
        p = capture_parsed_args(main, ["analyze_mutants", "src.py", "pytest"])
        self.assertIsNotNone(p)
        self.assertFalse(p.verbose)
        self.assertFalse(p.show)
        self.assertFalse(p.resume)
        self.assertFalse(p.noShuffle)
        self.assertIsNone(p.prefix)
        self.assertIsNone(p.fromFile)
        self.assertIsNone(p.seed)
        self.assertEqual(p.timeout, 30)
        self.assertEqual(p.numMutants, -1)
        self.assertIsNone(p.compileCommand)
        self.assertEqual(p.mutantDir, ".")
        self.assertIsNone(p.ignorefile)

    def test_check_covered_defaults(self):
        from universalmutator.checkcov import main
        p = capture_parsed_args(main, ["check_covered", "src.py", "cover.txt", "out.txt"])
        self.assertIsNotNone(p)
        self.assertEqual(p.mutantDir, ".")
        self.assertFalse(p.tstl)

    def test_prioritize_defaults(self):
        from universalmutator.prioritize import main
        p = capture_parsed_args(main, ["prioritize_mutants", "in.txt", "out.txt"])
        self.assertIsNotNone(p)
        self.assertFalse(p.verbose)
        self.assertFalse(p.noSDPriority)
        self.assertEqual(p.mutantDir, ".")
        self.assertEqual(p.sourceDir, ".")
        self.assertEqual(p.cutoff, 0.0)
        self.assertIsNone(p.N)

    def test_show_defaults(self):
        from universalmutator.show import main
        p = capture_parsed_args(main, ["show_mutants", "in.txt"])
        self.assertIsNotNone(p)
        self.assertFalse(p.concise)
        self.assertEqual(p.mutantDir, ".")
        self.assertEqual(p.sourceDir, ".")

    def test_prune_defaults(self):
        from universalmutator.prune import main
        p = capture_parsed_args(main, ["prune_mutants", "in.txt", "out.txt", "config.txt"])
        self.assertIsNotNone(p)
        self.assertEqual(p.mutantDir, ".")
        self.assertEqual(p.sourceDir, ".")


# 5. Flag and positional parsing
class TestFlagParsing(unittest.TestCase):

    def test_mutate_all_flags(self):
        from universalmutator.genmutants import main
        p = capture_parsed_args(main, [
            "mutate", "source.py",
            "--noCheck", "--comby", "--redundantOK", "--showRules",
            "--mutateInStrings", "--mutateTestCode", "--mutateBoth",
            "--noFastCheck", "--swap", "--tstl", "--fuzz", "--printStat",
            "--cmd", "compile MUTANT",
            "--lines", "lines.txt",
            "--mutantDir", "/tmp/mutants",
            "--ignore", "ignore.txt",
            "--compile", "compile.sol",
            "--only", "custom.rules",
        ])
        self.assertIsNotNone(p)
        self.assertTrue(p.noCheck)
        self.assertTrue(p.comby)
        self.assertTrue(p.redundantOK)
        self.assertTrue(p.showRules)
        self.assertTrue(p.mutateInStrings)
        self.assertTrue(p.mutateTestCode)
        self.assertTrue(p.mutateBoth)
        self.assertTrue(p.noFastCheck)
        self.assertTrue(p.swap)
        self.assertTrue(p.tstl)
        self.assertTrue(p.fuzz)
        self.assertTrue(p.printStat)
        self.assertEqual(p.cmd, "compile MUTANT")
        self.assertEqual(p.lines, "lines.txt")
        self.assertEqual(p.mutantDir, "/tmp/mutants")
        self.assertEqual(p.ignore, "ignore.txt")
        self.assertEqual(p.compile, "compile.sol")
        self.assertEqual(p.only, "custom.rules")

    def test_mutate_language_positional(self):
        from universalmutator.genmutants import main
        p = capture_parsed_args(main, ["mutate", "source.py", "python"])
        self.assertEqual(p.source, "source.py")
        self.assertEqual(p.language_or_rules, "python")
        self.assertEqual(p.rules, [])

    def test_mutate_extra_rules(self):
        from universalmutator.genmutants import main
        p = capture_parsed_args(main, ["mutate", "source.py", "python", "a.rules", "b.rules"])
        self.assertEqual(p.language_or_rules, "python")
        self.assertEqual(p.rules, ["a.rules", "b.rules"])

    def test_mutate_rules_file_as_language_or_rules(self):
        from universalmutator.genmutants import main
        p = capture_parsed_args(main, ["mutate", "source.py", "custom.rules"])
        self.assertEqual(p.language_or_rules, "custom.rules")

    def test_analyze_all_flags(self):
        from universalmutator.analyze import main
        p = capture_parsed_args(main, [
            "analyze_mutants", "src.py", "pytest",
            "--verbose", "--show", "--resume", "--noShuffle",
            "--prefix", "myprefix",
            "--fromFile", "mutants.txt",
            "--seed", "42",
            "--timeout", "60.5",
            "--numMutants", "100",
            "--compileCommand", "make",
            "--mutantDir", "./mutants",
        ])
        self.assertIsNotNone(p)
        self.assertTrue(p.verbose)
        self.assertTrue(p.show)
        self.assertTrue(p.resume)
        self.assertTrue(p.noShuffle)
        self.assertEqual(p.prefix, "myprefix")
        self.assertEqual(p.fromFile, "mutants.txt")
        self.assertEqual(p.seed, 42)
        self.assertAlmostEqual(p.timeout, 60.5)
        self.assertEqual(p.numMutants, 100)
        self.assertEqual(p.compileCommand, "make")
        self.assertEqual(p.mutantDir, "./mutants")

    def test_analyze_optional_ignorefile(self):
        from universalmutator.analyze import main
        p = capture_parsed_args(main, ["analyze_mutants", "src.py", "pytest", "ignore.txt"])
        self.assertEqual(p.ignorefile, "ignore.txt")

    def test_check_covered_tstl_flag(self):
        from universalmutator.checkcov import main
        p = capture_parsed_args(main, ["check_covered", "src.py", "cover.txt", "out.txt", "--tstl"])
        self.assertTrue(p.tstl)

    def test_check_covered_mutant_dir(self):
        from universalmutator.checkcov import main
        p = capture_parsed_args(main, ["check_covered", "src.py", "cover.txt", "out.txt",
                                       "--mutantDir", "./mymutants"])
        self.assertEqual(p.mutantDir, "./mymutants")

    def test_prioritize_with_N(self):
        from universalmutator.prioritize import main
        p = capture_parsed_args(main, ["prioritize_mutants", "in.txt", "out.txt", "50"])
        self.assertEqual(p.N, 50)

    def test_prioritize_all_flags(self):
        from universalmutator.prioritize import main
        p = capture_parsed_args(main, [
            "prioritize_mutants", "in.txt", "out.txt",
            "--verbose", "--noSDPriority",
            "--mutantDir", "./m",
            "--sourceDir", "./s",
            "--cutoff", "0.5",
        ])
        self.assertTrue(p.verbose)
        self.assertTrue(p.noSDPriority)
        self.assertEqual(p.mutantDir, "./m")
        self.assertEqual(p.sourceDir, "./s")
        self.assertAlmostEqual(p.cutoff, 0.5)

    def test_show_concise_flag(self):
        from universalmutator.show import main
        p = capture_parsed_args(main, ["show_mutants", "in.txt", "--concise"])
        self.assertTrue(p.concise)

    def test_show_dirs(self):
        from universalmutator.show import main
        p = capture_parsed_args(main, ["show_mutants", "in.txt",
                                       "--mutantDir", "./m", "--sourceDir", "./s"])
        self.assertEqual(p.mutantDir, "./m")
        self.assertEqual(p.sourceDir, "./s")

    def test_intersect_positionals(self):
        from universalmutator.intersect import main
        p = capture_parsed_args(main, ["intersect_mutants", "a.txt", "b.txt", "out.txt"])
        self.assertEqual(p.infile1, "a.txt")
        self.assertEqual(p.infile2, "b.txt")
        self.assertEqual(p.outfile, "out.txt")

    def test_find_missing_positionals(self):
        from universalmutator.findmissing import main
        p = capture_parsed_args(main, ["find_missing", "foo.py", "./dir1", "./dir2"])
        self.assertEqual(p.f, "foo.py")
        self.assertEqual(p.d1, "./dir1")
        self.assertEqual(p.d2, "./dir2")

    def test_prune_positionals_and_dirs(self):
        from universalmutator.prune import main
        p = capture_parsed_args(main, [
            "prune_mutants", "in.txt", "out.txt", "config.txt",
            "--mutantDir", "./m", "--sourceDir", "./s",
        ])
        self.assertEqual(p.infile, "in.txt")
        self.assertEqual(p.outfile, "out.txt")
        self.assertEqual(p.config, "config.txt")
        self.assertEqual(p.mutantDir, "./m")
        self.assertEqual(p.sourceDir, "./s")


# There are 45 tests in total, final output will be "OK" if they all pass
if __name__ == "__main__":
    unittest.main()
