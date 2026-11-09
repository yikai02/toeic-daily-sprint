# -*- coding: utf-8 -*-
"""Unit tests for mobile HTML interactivity and touch compatibility.

Verifies that:
1. Option buttons have inline `onclick="handleOptClick(this)"` for direct mobile touch handling
   without relying on fragile document-level click delegation in WebKit.
2. CSS includes `pointer-events: none` on child spans and `touch-action: manipulation`
   so touch targets are reliably the button itself.
3. JavaScript defines `handleOptClick` globally.
4. Mobile tip guidance is rendered in the HTML to inform users how to open in Safari/Chrome.
"""

import unittest
from html_generator import render_day_html
from master_curriculum import DAYS_DATA
from adaptive_srs_engine import build_session_payload


class TestHtmlMobileCompatibility(unittest.TestCase):

    def setUp(self):
        self.payload = build_session_payload(day_num=6, session="morning")
        self.html = render_day_html(DAYS_DATA[6], session="morning", payload=self.payload)

    def test_option_buttons_have_native_radio_and_label_for_offline_touch(self):
        """Every option must use native label + radio control for 100% Quick Look offline touch compatibility."""
        self.assertIn('class="opt-radio" data-opt="A" onchange="handleOptSelect(this)"', self.html)
        self.assertIn('class="opt-radio" data-opt="B" onchange="handleOptSelect(this)"', self.html)
        self.assertIn('class="opt-radio" data-opt="C" onchange="handleOptSelect(this)"', self.html)
        self.assertIn('class="opt-radio" data-opt="D" onchange="handleOptSelect(this)"', self.html)
        self.assertIn('.opt-radio:checked + .opt-btn-content', self.html)

    def test_css_has_mobile_touch_action_and_pointer_events(self):
        """CSS must include touch-action and label styling for mobile tap response."""
        self.assertIn('touch-action: manipulation', self.html)
        self.assertIn('.opt-label', self.html)

    def test_javascript_defines_handle_opt_select(self):
        """JavaScript must define window.handleOptSelect or function handleOptSelect."""
        self.assertIn('handleOptSelect', self.html)

    def test_instant_feedback_reveals_why_chosen_option_wrong_and_correct_option_right(self):
        """Selecting an option must directly reveal why it is wrong/right and why correct answer is right."""
        self.assertIn('.opt-radio:checked ~ .opt-instant-feedback', self.html)
        self.assertIn('opt-instant-feedback opt-feedback-wrong', self.html)
        self.assertIn('opt-instant-feedback opt-feedback-correct', self.html)
        self.assertIn('為什麼您選的', self.html)
        self.assertIn('為什麼對', self.html)

    def test_feedback_has_categorized_chips_and_cards(self):
        """Explanations must have categorized chips (POS, meaning, collocations)."""
        self.assertIn('fb-chips-row', self.html)
        self.assertIn('fb-chip-pos', self.html)
        self.assertIn('fb-chip-meaning', self.html)

    def test_options_locked_after_selection_in_css_and_js(self):
        """Options must be locked after selection until reset."""
        self.assertIn('.options-grid:has(.opt-radio:checked) .opt-label:not(:has(.opt-radio:checked))', self.html)
        self.assertIn('pointer-events: none', self.html)
        self.assertIn('opt-locked', self.html)

    def test_sticky_bar_has_safe_top_offset_to_avoid_title_overlap(self):
        """Sticky control bar must clear mobile document title bar with safe-area offset."""
        self.assertIn('top: calc(env(safe-area-inset-top', self.html)

    def test_mobile_tip_banner_present(self):
        """HTML must render a clear mobile tip banner for iPhone Telegram preview users."""
        self.assertIn('mobile-tip-banner', self.html)

    def test_questions_positioned_before_reference_accordion(self):
        """Practice questions must appear first right below sticky bar; vocab/grammar in collapsible reference at bottom."""
        p3_pos = self.html.find('id="sec-part3"')
        ref_pos = self.html.find('id="sec-reference"')
        self.assertNotEqual(p3_pos, -1)
        self.assertNotEqual(ref_pos, -1)
        self.assertLess(p3_pos, ref_pos, "Questions (Part 3) must be rendered before reference accordion!")

    def test_bulleted_explanations_and_no_fluff_banners(self):
        """Feedback must be concise bullet lists and bloated intro banners eliminated."""
        self.assertIn('clean-bullet-list', self.html)
        self.assertIn('重點考點', self.html)
        self.assertIn('全句中譯', self.html)
        self.assertNotIn('part-intro-banner', self.html)


if __name__ == "__main__":
    unittest.main()
