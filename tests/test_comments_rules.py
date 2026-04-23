# This file is to test comment format for .rules files as stated in (Issue 23)
import unittest
import io
import sys
import tempfile
import os

from universalmutator.mutator import parseRules

# written tests, still not tested!

class TestParseRulesComments(unittest.TestCase):

    def _parse(self, rule_text):
        """
        Helper: write rules to temp file, run parseRules, capture stdout
        """
        fd, path = tempfile.mkstemp(suffix=".rules")
        os.close(fd)

        try:
            with open(path, "w") as f:
                f.write(rule_text)

            # capture print output
            buffer = io.StringIO()
            old_stdout = sys.stdout
            sys.stdout = buffer

            try:
                rules, ignoreRules, skipRules = parseRules([path])
            finally:
                sys.stdout = old_stdout

            return rules, ignoreRules, skipRules, buffer.getvalue()

        finally:
            os.remove(path)

    # ---------------------------------------------------
    # TEST 1: indented comments should be ignored
    # ---------------------------------------------------
    def test_indented_comments_ignored(self):
        rules, ignoreRules, skipRules, out = self._parse(
            "   # comment line\n"
            "\t# tab comment\n"
            "\\+ ==> -\n"
        )

        self.assertEqual(len(rules), 1)
        self.assertEqual(len(ignoreRules), 0)
        self.assertEqual(len(skipRules), 0)

    # ---------------------------------------------------
    # TEST 2: blank lines should be ignored
    # ---------------------------------------------------
    def test_blank_lines_ignored(self):
        rules, _, _, out = self._parse(
            "\\+ ==> -\n"
            "\n"
            "   \n"
            "\\* ==> /\n"
        )

        self.assertEqual(len(rules), 2)

    # ---------------------------------------------------
    # TEST 3: rules starting with '#' must NOT be treated as comments
    # ---------------------------------------------------
    def test_hash_rules_still_parse(self):
        rules, ignoreRules, skipRules, out = self._parse(
            "#include ==> DO_NOT_MUTATE\n"
            "# ==> SKIP_MUTATING_REST\n"
        )

        self.assertEqual(len(ignoreRules), 1)
        self.assertEqual(len(skipRules), 1)


if __name__ == "__main__":
    unittest.main()