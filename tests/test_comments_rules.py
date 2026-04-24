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
            "\t\n"
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

    # ---------------------------------------------------
    # TEST 4: only comments should result in no rules and no warnings
    # ---------------------------------------------------

    def test_only_comments(self):
        rules, ignoreRules, skipRules, out = self._parse(
            "# comment\n"
            "   # indented comment\n"
            " # spaced comment\n"
            "#\t tab comment\n"
        )

        self.assertEqual(len(rules), 0)
        self.assertEqual(len(ignoreRules), 0)
        self.assertEqual(len(skipRules), 0)

    # ---------------------------------------------------
    # TEST 5: Invalid lines should still warn, but not be treated as rules
    # ---------------------------------------------------
    def test_invalid_lines(self):
        rules, ignoreRules, skipRules, out = self._parse(
            "   # comment line\n"
            "\t# tab comment\n"
            "\\+ ==> -\n"
            "# ==> SKIP_MUTATING_REST\n"
            "invalid line\n"
        )

        self.assertEqual(len(rules), 1)
        self.assertEqual(len(ignoreRules), 0)
        self.assertEqual(len(skipRules), 1)

    # ---------------------------------------------------
    # TEST 6: Mixed file test with comments, blank lines, valid rules, and invalid lines
    # ---------------------------------------------------
    def test_mixed_file(self):
        rules, ignoreRules, skipRules, out = self._parse(
            "# comment\n"
            "\n"
            "   # indented comment\n"
            " # spaced comment\n"
            "\\+ ==> -\n"
            "invalid line\n"
            "# ==> SKIP_MUTATING_REST\n"
        )

        self.assertEqual(len(rules), 1)
        self.assertEqual(len(ignoreRules), 0)
        self.assertEqual(len(skipRules), 1)

    # ---------------------------------------------------
    # TEST 7: Disabled rules should be ignored, but still treated as comments
    # ---------------------------------------------------
    def test_disabled_rules_ignored(self):
        rules, ignoreRules, skipRules, out = self._parse(
            "#DISABLED: \\+ ==> -\n"
            "#DISABLED: #include ==> DO_NOT_MUTATE\n"
            "#DISABLED: # ==> SKIP_MUTATING_REST\n"
            "\\* ==> /\n"
        )

        self.assertEqual(len(rules), 1)
        self.assertEqual(len(ignoreRules), 0)
        self.assertEqual(len(skipRules), 0)

    # ---------------------------------------------------
    # TEST 8: Disabled rules with different spacing should still be ignored (MAYBE?) Might be  problems
    # ---------------------------------------------------
    def test_disabled_rules_varied_spacing(self):
        rules, ignoreRules, skipRules, out = self._parse(
            "\t\t\t#DISABLED: \\+ ==> -\n"
            "  #DISABLED: #include ==> DO_NOT_MUTATE\n"
            "\t#DISABLED: # ==> SKIP_MUTATING_REST\n"
            "\\* ==> /\n"
        )

        self.assertEqual(len(rules), 1)
        self.assertEqual(len(ignoreRules), 0)
        self.assertEqual(len(skipRules), 0)

    # ---------------------------------------------------
    # TEST 9: Header Testing with comments, blank lines before and after header, and example rules comments
    # ---------------------------------------------------
    def test_header_with_comments_and_blank_lines(self):
        rules, ignoreRules, skipRules, out = self._parse(
            "# This is a header comment\n"
            "# It should be ignored\n"
            "\n"
            "# Another header comment\n"
            "\n"
            "# Example rule comment\n"
            "#DISABLED: <code expression> ==> <replacement>\n"
            "# This is an example rule that should be ignored\n"
            "#DISABLED: #include ==> DO_NOT_MUTATE\n"
        )

        self.assertEqual(len(rules), 1)
        self.assertEqual(len(ignoreRules), 0)
        self.assertEqual(len(skipRules), 0)

    # ---------------------------------------------------
    # TEST 10: Larger file test with multiple comments, blank lines, valid rules, invalid lines, and disabled rules
    # ---------------------------------------------------
    def test_larger_mixed_file(self):
        rules, ignoreRules, skipRules, out = self._parse(
            "# =====================================================\n"
            "# HEADER COMMENT BLOCK\n"
            "# This file tests real-world mixed .rules behavior\n"
            "# =====================================================\n"
            "\n"
            "# Simple arithmetic rules\n"
            "\\+ ==> -\n"
            "\\- ==> +\n"
            "\n"
            "# multiplication and division\n"
            "\\* ==> /\n"
            "\\/ ==> *\n"
            "\n"
            "   # indented comment inside file\n"
            "\t# tab-indented comment\n"
            "\n"
            "# Disabled rule section\n"
            "# DISABLED: \\+ ==> *\n"
            "# DISABLED: \\* ==> +\n"
            "\n"
            "# Special ignore rule\n"
            "#include ==> DO_NOT_MUTATE\n"
            "\n"
            "# Special skip rule\n"
            "# ==> SKIP_MUTATING_REST\n"
            "\n"
            "# Invalid lines (should trigger warnings)\n"
            "this is not a rule\n"
            "==> broken rule\n"
            "\\+ == bad format\n"
            "\n"
            "# More valid rules\n"
            "== ==> !=\n"
            "!= ==> ==\n"
            "< ==> >\n"
            "> ==> <\n"
            "\n"
            "# More noise\n"
            "random text here\n"
            "another bad line\n"
            "\n"
            "# Final valid rule\n"
            "\\% ==> +\n"
        )

        # Expected valid rules:
        # +, -, *, /, ==, !=, <, >, %
        self.assertEqual(len(rules), 9)

        # Only one ignore rule (#include ==> DO_NOT_MUTATE)
        self.assertEqual(len(ignoreRules), 1)

        # Only one skip rule (# ==> SKIP_MUTATING_REST)
        self.assertEqual(len(skipRules), 1)

if __name__ == "__main__":
    unittest.main()