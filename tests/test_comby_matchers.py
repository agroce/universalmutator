import shutil
import sys
import uuid
from pathlib import Path
from unittest import TestCase, mock

from universalmutator import genmutants


class TestCombyMatchers(TestCase):
    def test_comby_matcher_helper_falls_back_for_unsupported_extensions(self):
        self.assertEqual(genmutants.combyMatcherFor("func", ".fc"), ".generic")
        self.assertEqual(genmutants.combyMatcherFor("tact", ".tact"), ".generic")
        self.assertEqual(genmutants.combyMatcherFor("tolk", ".tolk"), ".generic")
        self.assertEqual(genmutants.combyMatcherFor("c", ".h"), ".c")
        self.assertEqual(genmutants.combyMatcherFor("javascript", ".ts"), ".ts")

    def test_main_passes_resolved_comby_matcher(self):
        tmpdir = Path("tests") / (".tmp_comby_matcher_" + uuid.uuid4().hex)
        tmpdir.mkdir(parents=True)
        try:
            source_path = tmpdir / "sample.fc"
            mutant_dir = tmpdir / "mutants"
            source_path.write_text("() main() {\n}\n", encoding="utf-8")

            captured = {}

            def fake_mutants(source, ruleFiles=None, **kwargs):
                captured["language"] = kwargs["language"]
                return []

            argv = [
                "mutate",
                str(source_path),
                "func",
                "--comby",
                "--noCheck",
                "--mutantDir",
                str(mutant_dir),
            ]
            with mock.patch.object(sys, "argv", argv):
                with mock.patch.object(genmutants.mutator, "mutants_comby", side_effect=fake_mutants):
                    genmutants.main()

            self.assertEqual(captured["language"], ".generic")
        finally:
            shutil.rmtree(str(tmpdir), ignore_errors=True)
