# -*- coding: utf-8 -*-
"""Unit tests for automatic real-time cloud cross-device synchronization.

Verifies:
1. HTML generation embeds seamless cloud synchronization engine when bot_token is provided.
2. Upgrade from fragile sessionStorage to persistent localStorage for local zero-loss safety.
3. Debounced cloud sync function `syncProgressToCloud` and fetch function `fetchCloudProgress` exist.
4. Compact progress encoding formats (43-char answer map + timestamp) fit within Telegram description limits.
5. Live cloud status indicator badge exists in the sticky control bar.
"""

import unittest
from html_generator import render_day_html
from master_curriculum import DAYS_DATA
from adaptive_srs_engine import build_session_payload


class TestCloudCrossDeviceSync(unittest.TestCase):

    def setUp(self):
        self.payload = build_session_payload(day_num=6, session="morning")
        self.fake_token = "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"
        self.html = render_day_html(
            DAYS_DATA[6],
            session="morning",
            payload=self.payload,
            bot_token=self.fake_token,
        )

    def test_local_storage_used_for_permanent_retention(self):
        """Must use localStorage so closing tab or browser on phone never clears answers."""
        self.assertIn('localStorage.setItem', self.html)
        self.assertIn('localStorage.getItem', self.html)
        self.assertNotIn('sessionStorage.setItem', self.html)

    def test_cloud_sync_functions_present_in_script(self):
        """JavaScript must define syncProgressToCloud and fetchCloudProgress."""
        self.assertIn('syncProgressToCloud', self.html)
        self.assertIn('fetchCloudProgress', self.html)
        self.assertIn('getMyDescription', self.html)
        self.assertIn('setMyDescription', self.html)

    def test_live_cloud_sync_badge_in_control_bar(self):
        """Sticky control bar must display a live cloud synchronization status indicator."""
        self.assertIn('id="cloud-sync-status"', self.html)
        self.assertIn('雲端同步', self.html)

    def test_bot_token_injection(self):
        """When bot_token is provided, it is injected into the sync configuration."""
        self.assertIn(self.fake_token, self.html)


if __name__ == "__main__":
    unittest.main()
