#!/usr/bin/env python
"""Tests for review-context script — path construction and tmp/ usage."""
import os
import sys
import unittest

SCRIPT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "review-context")


def _load_checkout_state_path():
    """Load the review-context script and return its checkout_state_path function."""
    ns = {}
    with open(SCRIPT) as f:
        exec(f.read(), ns)
    return ns["checkout_state_path"]


checkout_state_path = staticmethod(_load_checkout_state_path())


class TestCheckoutStatePath(unittest.TestCase):
    """Tests for checkout_state_path() — the path that must use tmp/ not .claude/."""

    def test_uses_tmp_dir(self):
        """checkout_state_path must use tmp/_review-artifacts, not .claude/_review-artifacts."""
        path = checkout_state_path("/some/repo", "42")
        self.assertIn("tmp", path)
        self.assertIn("_review-artifacts", path)
        self.assertNotIn(".claude", path)

    def test_ends_with_checkout_state_json(self):
        """Path must end with checkout-state-<pr>.json."""
        path = checkout_state_path("/repo", "99")
        self.assertTrue(path.endswith("checkout-state-99.json"))

    def test_joins_root_correctly(self):
        """Path must be rooted at the given repo root."""
        path = checkout_state_path("/my/project", "7")
        expected = os.path.join("/my/project", "tmp", "_review-artifacts", "checkout-state-7.json")
        self.assertEqual(path, expected)

    def test_does_not_contain_claude(self):
        """Regression: ensure .claude never appears in the path."""
        path = checkout_state_path("/any/repo", "1")
        self.assertNotIn(".claude", path)


if __name__ == "__main__":
    unittest.main()
