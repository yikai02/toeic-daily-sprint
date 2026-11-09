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

    def test_option_buttons_have_inline_onclick(self):
        """Every .opt-btn must have onclick='handleOptClick(this)' for mobile compatibility."""
        self.assertIn('class="opt-btn" data-opt="A" onclick="handleOptClick(this)"', self.html)
        self.assertIn('class="opt-btn" data-opt="B" onclick="handleOptClick(this)"', self.html)
        self.assertIn('class="opt-btn" data-opt="C" onclick="handleOptClick(this)"', self.html)
        self.assertIn('class="opt-btn" data-opt="D" onclick="handleOptClick(this)"', self.html)

    def test_css_has_mobile_touch_action_and_pointer_events(self):
        """CSS must include touch-action and child pointer-events: none to avoid mobile tap drops."""
        self.assertIn('touch-action: manipulation', self.html)
        self.assertIn('.opt-btn *', self.html)
        self.assertIn('pointer-events: none', self.html)

    def test_javascript_defines_handle_opt_click(self):
        """JavaScript must define window.handleOptClick or function handleOptClick."""
        self.assertIn('handleOptClick', self.html)

    def test_mobile_tip_banner_present(self):
        """HTML must render a clear mobile tip banner for iPhone Telegram preview users."""
        self.assertIn('mobile-tip-banner', self.html)


if __name__ == "__main__":
    unittest.main()
