#!/usr/bin/env python
"""Tests for review-filter decision table logic."""
import importlib
import json
import subprocess
import sys
import os
import tempfile
import unittest

SCRIPT = os.path.join(os.path.dirname(__file__), "review-filter")

# Minimal issue that passes all gates except the one under test.
PASSING = {
    "id": "1",
    "on_modified_lines": True,
    "requires_on_modified_lines": True,
    "pre_existing": False,
    "caught_by_tooling": False,
    "verified_by_reading_file": True,
    "code_confirms_issue": True,
    "has_direct_evidence_quote": True,
    "practical_impact": "high",
    "claude_md_relevance": "none",
}


def _load_keep():
    """Load the hyphenated review-filter script and return its keep function."""
    ns = {}
    with open(os.path.join(os.path.dirname(__file__), "review-filter")) as f:
        exec(f.read(), ns)
    return ns["keep"]


class TestKeepFunction(unittest.TestCase):
    """Direct unit tests of the keep() function."""

    keep = staticmethod(_load_keep())

    def test_passing_issue_survives(self):
        self.assertTrue(self.keep(PASSING))

    # --- on_modified_lines gate ---

    def test_on_modified_lines_false_rejects_by_default(self):
        issue = {**PASSING, "on_modified_lines": False}
        self.assertFalse(self.keep(issue))

    def test_on_modified_lines_true_passes(self):
        issue = {**PASSING, "on_modified_lines": True}
        self.assertTrue(self.keep(issue))

    # --- requires_on_modified_lines bypass ---

    def test_compliance_issue_bypasses_on_modified_lines(self):
        """A diff-agnostic finding (requires_on_modified_lines=False)
        should survive even when on_modified_lines is False."""
        issue = {**PASSING, "on_modified_lines": False, "requires_on_modified_lines": False}
        self.assertTrue(self.keep(issue))

    def test_requires_on_modified_lines_explicit_true_unchanged(self):
        """Explicit requires_on_modified_lines=True behaves like default."""
        issue = {**PASSING, "on_modified_lines": True, "requires_on_modified_lines": True}
        self.assertTrue(self.keep(issue))

    def test_requires_on_modified_lines_explicit_true_rejects_off_lines(self):
        """Explicit requires_on_modified_lines=True still rejects off-line issues."""
        issue = {**PASSING, "on_modified_lines": False, "requires_on_modified_lines": True}
        self.assertFalse(self.keep(issue))

    def test_backward_compat_missing_requires_field(self):
        """Old issues without requires_on_modified_lines default to True,
        so on_modified_lines must still be True."""
        issue = {k: v for k, v in PASSING.items() if k != "requires_on_modified_lines"}
        # on_modified_lines=True should pass
        self.assertTrue(self.keep(issue))
        # on_modified_lines=False should fail
        issue = {**issue, "on_modified_lines": False}
        self.assertFalse(self.keep(issue))

    # --- other gates ---

    def test_pre_existing_rejected(self):
        issue = {**PASSING, "pre_existing": True}
        self.assertFalse(self.keep(issue))

    def test_caught_by_tooling_rejected(self):
        issue = {**PASSING, "caught_by_tooling": True}
        self.assertFalse(self.keep(issue))

    def test_unverified_rejected(self):
        issue = {**PASSING, "verified_by_reading_file": False}
        self.assertFalse(self.keep(issue))

    def test_code_does_not_confirm_rejected(self):
        issue = {**PASSING, "code_confirms_issue": False}
        self.assertFalse(self.keep(issue))

    def test_no_evidence_quote_rejected(self):
        issue = {**PASSING, "has_direct_evidence_quote": False}
        self.assertFalse(self.keep(issue))

    def test_medium_impact_without_claude_md_rejected(self):
        issue = {**PASSING, "practical_impact": "medium", "claude_md_relevance": "none"}
        self.assertFalse(self.keep(issue))

    def test_medium_impact_with_related_claude_md_rejected(self):
        issue = {**PASSING, "practical_impact": "medium", "claude_md_relevance": "related"}
        self.assertFalse(self.keep(issue))

    def test_medium_impact_with_explicit_claude_md_passes(self):
        issue = {**PASSING, "practical_impact": "medium", "claude_md_relevance": "explicit"}
        self.assertTrue(self.keep(issue))

    def test_low_impact_with_explicit_claude_md_passes(self):
        issue = {**PASSING, "practical_impact": "low", "claude_md_relevance": "explicit"}
        self.assertTrue(self.keep(issue))

    def test_compliance_issue_still_rejected_if_pre_existing(self):
        """Compliance bypass only affects on_modified_lines; other gates still apply."""
        issue = {**PASSING, "on_modified_lines": False, "requires_on_modified_lines": False, "pre_existing": True}
        self.assertFalse(self.keep(issue))

    def test_compliance_issue_still_rejected_if_caught_by_tooling(self):
        issue = {**PASSING, "on_modified_lines": False, "requires_on_modified_lines": False, "caught_by_tooling": True}
        self.assertFalse(self.keep(issue))


class TestCLIFilter(unittest.TestCase):
    """Integration tests running the script as a subprocess."""

    def _run(self, issues, args=None):
        payload = json.dumps(issues)
        cmd = [sys.executable, SCRIPT]
        if args:
            cmd.extend(args)
        result = subprocess.run(cmd, input=payload, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(result.stdout)

    def test_cli_filters_issues(self):
        issues = [PASSING, {**PASSING, "on_modified_lines": False}]
        survivors = self._run(issues)
        self.assertEqual(len(survivors), 1)
        self.assertEqual(survivors[0]["id"], "1")

    def test_cli_file_input(self):
        fd, path = tempfile.mkstemp(suffix=".json")
        try:
            with open(fd, "w") as f:
                json.dump([PASSING], f)
            result = subprocess.run(
                [sys.executable, SCRIPT, path], capture_output=True, text=True
            )
            self.assertEqual(result.returncode, 0)
            survivors = json.loads(result.stdout)
            self.assertEqual(len(survivors), 1)
        finally:
            os.unlink(path)

    def test_cli_usage_error(self):
        result = subprocess.run([sys.executable, SCRIPT, "a", "b"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)

    def test_cli_compliance_issue_survives(self):
        compliance = {**PASSING, "on_modified_lines": False, "requires_on_modified_lines": False}
        survivors = self._run([compliance])
        self.assertEqual(len(survivors), 1)

    def test_cli_empty_input(self):
        survivors = self._run([])
        self.assertEqual(survivors, [])


if __name__ == "__main__":
    unittest.main()