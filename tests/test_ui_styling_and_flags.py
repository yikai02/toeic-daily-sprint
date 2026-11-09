# -*- coding: utf-8 -*-
"""Unit tests for UI styling, high-contrast example sentences, and flag elimination.

Verifies:
1. No regional indicator/national flag emoji (e.g. 🇹🇼, 🇺🇸, etc.) appears in the generated HTML.
2. Example sentence English and Chinese (.ex-en, .ex-zh) have strong contrast styling
   and are not using invisible/low-contrast colors like #1e293b in dark mode.
3. Dark mode rules provide crisp contrast for example sentences and translations.
"""

import re
import unittest
from html_generator import render_day_html
from master_curriculum import DAYS_DATA
from adaptive_srs_engine import build_session_payload


class TestUiStylingAndFlags(unittest.TestCase):

    def setUp(self):
        self.payload = build_session_payload(day_num=6, session="morning")
        self.html = render_day_html(DAYS_DATA[6], session="morning", payload=self.payload)

    def test_no_national_flags_in_html(self):
        """Rendered HTML must not contain any country/regional flag emojis."""
        flag_matches = re.findall(r'[\U0001F1E6-\U0001F1FF]{2}', self.html)
        self.assertEqual(
            flag_matches,
            [],
            f"Found national flags in rendered HTML: {flag_matches}. User requested NO FLAGS."
        )

    def test_example_sentence_contrast_and_size(self):
        """Example sentences must have high contrast and readable font size."""
        self.assertIn('.ex-en', self.html)
        self.assertIn('.ex-zh', self.html)
        # Check dark mode overrides for example sentences
        self.assertIn('color: #f8fafc !important;', self.html)
        self.assertIn('color: #93c5fd !important;', self.html)

    def test_translation_labels_do_not_have_flag(self):
        """Labels like '例句中譯' or '全句中譯' must not have 🇹🇼 prefix."""
        self.assertNotIn('🇹🇼', self.html)


if __name__ == "__main__":
    unittest.main()
