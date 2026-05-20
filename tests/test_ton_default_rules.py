from __future__ import print_function

import shutil
import sys
import uuid
from pathlib import Path
from unittest import TestCase, mock

from universalmutator import genmutants
from universalmutator import mutator


class TestTonDefaultRules(TestCase):
    def _capture_default_rules(self, suffix, source_text):
        tmpdir = Path("tests") / (".tmp_ton_rules_" + uuid.uuid4().hex)
        tmpdir.mkdir(parents=True)
        try:
            source_path = tmpdir / ("sample" + suffix)
            mutant_dir = tmpdir / "mutants"
            source_path.write_text(source_text, encoding="utf-8")

            captured = {}

            def fake_mutants(source, ruleFiles=None, **kwargs):
                captured["ruleFiles"] = list(ruleFiles)
                return []

            argv = [
                "mutate",
                str(source_path),
                "--noCheck",
                "--mutantDir",
                str(mutant_dir),
            ]
            with mock.patch.object(sys, "argv", argv):
                with mock.patch.object(genmutants.mutator, "mutants_regexp", side_effect=fake_mutants):
                    genmutants.main()

            return captured["ruleFiles"]
        finally:
            shutil.rmtree(str(tmpdir), ignore_errors=True)

    def test_ton_languages_use_ton_common_by_default(self):
        tact_rules = self._capture_default_rules(".tact", "contract Sample {}\n")
        func_rules = self._capture_default_rules(".fc", "() main() {\n}\n")
        tolk_rules = self._capture_default_rules(".tolk", "fun main() {\n}\n")

        self.assertEqual(tact_rules[:2], ["ton_common.rules", "tact.rules"])
        self.assertEqual(func_rules[:2], ["ton_common.rules", "func.rules"])
        self.assertEqual(tolk_rules[:2], ["ton_common.rules", "tolk.rules"])

        for rules in (tact_rules, func_rules, tolk_rules):
            self.assertNotIn("universal.rules", rules)
            self.assertNotIn("c_like.rules", rules)

    def test_non_ton_defaults_still_use_universal_and_c_like(self):
        c_rules = self._capture_default_rules(".c", "int main() { return 0; }\n")

        self.assertEqual(c_rules[:2], ["universal.rules", "c.rules"])
        self.assertIn("c_like.rules", c_rules)

    def test_ton_common_regex_rules_generate_expected_mutants(self):
        source = [
            "if (cond) {\n",
            "    break;\n",
            "}\n",
            "while (flag) {\n",
            "    continue;\n",
            "}\n",
            "let both = left && right;\n",
            "let eq = a == b;\n",
            "let ge = a >= b;\n",
            "let sum = a + b;\n",
            "let diff = a - b;\n",
            "let mul = a * b;\n",
            "let div = a / b;\n",
            "let band = a & b;\n",
            "count += 1;\n",
            "mask <<= 1;\n",
        ]

        mutants = mutator.mutants_regexp(
            source,
            ruleFiles=["ton_common.rules"],
            ignorePatterns=[],
        )
        mutant_lines = {mutant[1].rstrip() for mutant in mutants}

        self.assertNotIn("if (!(cond)) {", mutant_lines)
        self.assertNotIn("if (0==1) {", mutant_lines)
        self.assertIn("    continue;", mutant_lines)
        self.assertIn("    break;", mutant_lines)
        self.assertIn("let both = left || right;", mutant_lines)
        self.assertIn("let eq = a != b;", mutant_lines)
        self.assertIn("let ge = a > b;", mutant_lines)
        self.assertIn("let sum = a - b;", mutant_lines)
        self.assertIn("let diff = a + b;", mutant_lines)
        self.assertIn("let mul = a / b;", mutant_lines)
        self.assertIn("let div = a * b;", mutant_lines)
        self.assertIn("let band = a | b;", mutant_lines)
        self.assertIn("count -= 1;", mutant_lines)
        self.assertIn("mask >>= 1;", mutant_lines)
        self.assertIn("while (false) {", mutant_lines)

    def test_ton_comby_uses_generic_matcher_for_unsupported_extensions(self):
        cases = [
            (".tact", "contract Sample {}\n", "tact.rules"),
            (".fc", "() main() {\n}\n", "func.rules"),
            (".tolk", "fun main() {\n}\n", "tolk.rules"),
        ]

        for suffix, source_text, lang_rule in cases:
            tmpdir = Path("tests") / (".tmp_ton_comby_" + uuid.uuid4().hex)
            tmpdir.mkdir(parents=True)
            try:
                source_path = tmpdir / ("sample" + suffix)
                mutant_dir = tmpdir / "mutants"
                source_path.write_text(source_text, encoding="utf-8")

                captured = {}

                # pylint: disable=cell-var-from-loop
                def fake_mutants(source, ruleFiles=None, **kwargs):
                    captured["ruleFiles"] = list(ruleFiles)
                    captured["language"] = kwargs["language"]
                    return []

                argv = [
                    "mutate",
                    str(source_path),
                    "--comby",
                    "--noCheck",
                    "--mutantDir",
                    str(mutant_dir),
                ]
                with mock.patch.object(sys, "argv", argv):
                    with mock.patch.object(genmutants.mutator, "mutants_comby", side_effect=fake_mutants):
                        genmutants.main()

                self.assertEqual(captured["ruleFiles"][:2], ["ton_common.rules", lang_rule])
                self.assertEqual(captured["language"], ".generic")
            finally:
                shutil.rmtree(str(tmpdir), ignore_errors=True)
