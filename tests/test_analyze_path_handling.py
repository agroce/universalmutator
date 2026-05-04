import os
import sys
import tempfile
from unittest import TestCase, mock

from universalmutator import analyze


class TestAnalyzePathHandling(TestCase):
    def test_analyze_writes_basename_for_windows_style_mutant_paths(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            original_cwd = os.getcwd()
            os.chdir(temp_dir)
            try:
                os.makedirs("contracts", exist_ok=True)
                with open(os.path.join("contracts", "temp.tolk"), "w") as f:
                    f.write("fun main() {}\n")

                argv = [
                    "analyze_mutants",
                    "contracts/temp.tolk",
                    'python MUTANT',
                    "--mutantDir",
                    "mutants",
                    "--noShuffle",
                ]

                with mock.patch.object(sys, "argv", argv):
                    with mock.patch.object(
                        analyze.glob,
                        "glob",
                        return_value=[r"mutants\temp.mutant.0.tolk"],
                    ):
                        with mock.patch.object(
                            analyze.subprocess,
                            "Popen",
                            return_value=mock.Mock(returncode=0, poll=mock.Mock(return_value=0)),
                        ):
                            analyze.main()

                with open("notkilled.txt", "r") as f:
                    self.assertEqual(f.read().strip(), "temp.mutant.0.tolk")
            finally:
                os.chdir(original_cwd)
