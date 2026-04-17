"""Tests for comment and blank-line handling in rule files (issue #23).

These tests verify parseRules() correctly:
  * treats lines beginning with '#' (optionally indented) as comments
  * skips blank and whitespace-only lines without warning
  * continues to parse existing rules whose LHS starts with '#'
    (e.g. '#include ==> DO_NOT_MUTATE', '# ==> SKIP_MUTATING_REST')
  * still warns on genuinely malformed rule lines
"""
from __future__ import print_function

import io
import os
import sys
import tempfile
import unittest

from universalmutator.mutator import parseRules


class TestRuleComments(unittest.TestCase):

    def _parse(self, rule_text):
        """Write rule_text to a temp .rules file, call parseRules, return
        (rules, ignoreRules, skipRules, captured_stdout)."""
        fd, path = tempfile.mkstemp(suffix=".rules")
        os.close(fd)
        try:
            with open(path, "w") as f:
                f.write(rule_text)
            buf = io.StringIO()
            orig_stdout = sys.stdout
            sys.stdout = buf
            try:
                rules, ignoreRules, skipRules = parseRules([path])
            finally:
                sys.stdout = orig_stdout
            return rules, ignoreRules, skipRules, buf.getvalue()
        finally:
            os.unlink(path)

    def assertNoMalformedWarning(self, output):
        self.assertNotIn(
            "DOES NOT MATCH EXPECTED FORMAT", output,
            "parseRules printed a malformed-rule warning but should not have:\n"
            + output)

    # --- Comments at start of line ---------------------------------------

    def test_plain_hash_comment_is_ignored(self):
        rules, _, _, out = self._parse(
            "# a plain comment\n"
            "\\+ ==> -\n"
        )
        self.assertEqual(len(rules), 1)
        self.assertNoMalformedWarning(out)

    def test_indented_hash_comment_is_ignored(self):
        rules, _, _, out = self._parse(
            "    # indented comment with 4 spaces\n"
            "\t# tab-indented comment\n"
            "\\+ ==> -\n"
        )
        self.assertEqual(len(rules), 1)
        self.assertNoMalformedWarning(out)

    def test_multiple_comments_do_not_produce_rules(self):
        rules, ignoreRules, skipRules, out = self._parse(
            "# comment one\n"
            "# comment two\n"
            "# comment three\n"
        )
        self.assertEqual(len(rules), 0)
        self.assertEqual(len(ignoreRules), 0)
        self.assertEqual(len(skipRules), 0)
        self.assertNoMalformedWarning(out)

    # --- Blank lines ------------------------------------------------------

    def test_empty_blank_line_is_ignored(self):
        rules, _, _, out = self._parse(
            "\\+ ==> -\n"
            "\n"
            "\\* ==> /\n"
        )
        self.assertEqual(len(rules), 2)
        self.assertNoMalformedWarning(out)

    def test_whitespace_only_line_is_ignored(self):
        rules, _, _, out = self._parse(
            "\\+ ==> -\n"
            "    \n"
            "\t\t\n"
            "\\* ==> /\n"
        )
        self.assertEqual(len(rules), 2)
        self.assertNoMalformedWarning(out)

    # --- Backward compatibility: LHS starting with '#' --------------------

    def test_hash_include_rule_still_parses_as_ignore(self):
        """c_like.rules contains '#include ==> DO_NOT_MUTATE' — must not
        be mistaken for a comment."""
        _, ignoreRules, _, out = self._parse("#include ==> DO_NOT_MUTATE\n")
        self.assertEqual(len(ignoreRules), 1)
        self.assertNoMalformedWarning(out)

    def test_bare_hash_skip_rule_still_parses_as_skip(self):
        """python.rules contains '# ==> SKIP_MUTATING_REST' — must not
        be mistaken for a comment."""
        _, _, skipRules, out = self._parse("# ==> SKIP_MUTATING_REST\n")
        self.assertEqual(len(skipRules), 1)
        self.assertNoMalformedWarning(out)

    # --- Mixed content ----------------------------------------------------

    def test_header_comment_block_and_rules(self):
        """Realistic case: documentation header plus rules."""
        rules, ignoreRules, skipRules, out = self._parse(
            "# ============================================\n"
            "# Universal rules for arithmetic operator swaps\n"
            "# ============================================\n"
            "\n"
            "# Addition to other operators\n"
            "\\+ ==> -\n"
            "\\+ ==> *\n"
            "\n"
            "# Skip rest of line after Python '#' comment\n"
            "# ==> SKIP_MUTATING_REST\n"
        )
        self.assertEqual(len(rules), 2)
        self.assertEqual(len(skipRules), 1)
        self.assertNoMalformedWarning(out)

    # --- Warnings still fire for bad input --------------------------------

    def test_malformed_line_still_warns(self):
        """A line with no '==>' and not a comment should still warn."""
        _, _, _, out = self._parse("this line is not a rule\n")
        self.assertIn("DOES NOT MATCH EXPECTED FORMAT", out)


if __name__ == "__main__":
    unittest.main()
