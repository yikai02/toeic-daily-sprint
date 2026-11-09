# -*- coding: utf-8 -*-
"""Unit tests for dispatch scheduling resilience, cron resolution, and idempotency.

Follows Test-Driven Development (TDD) principles to guarantee that:
1. All staggered GitHub Actions crons (morning and afternoon windows) correctly resolve
   to their intended sessions, even under extreme queue delays (3-6+ hours).
2. Explicit session overrides (e.g. from workflow_dispatch) take precedence.
3. Fallback logic correctly uses Taipei time when no cron is specified.
4. Multiple rapid/staggered triggers within the same window are safely deduplicated
   by cloud idempotency guards without re-sending or raising unhandled errors.
"""

import unittest
from datetime import datetime
from unittest.mock import MagicMock, patch
from zoneinfo import ZoneInfo

import dispatch_runner

TZ = ZoneInfo("Asia/Taipei")


class TestDispatchScheduling(unittest.TestCase):

    def test_staggered_morning_crons_resolve_to_morning_even_when_delayed(self):
        """Morning crons must resolve to 'morning' regardless of execution hour."""
        morning_crons = [
            "45 23 * * *",
            "50 23 * * *",
            "55 23 * * *",
            "58 23 * * *",
            "0 0 * * *",
            "5 0 * * *",
            "10 0 * * *",
            "20 0 * * *",
            "30 0 * * *",
            "0 1 * * *",
        ]
        # Delayed times: 08:00, 11:30, 12:45, 14:30, 16:00 Taipei time
        delayed_times = [
            datetime(2026, 11, 9, 8, 0, tzinfo=TZ),
            datetime(2026, 11, 9, 11, 30, tzinfo=TZ),
            datetime(2026, 11, 9, 12, 45, tzinfo=TZ),
            datetime(2026, 11, 9, 14, 30, tzinfo=TZ),
            datetime(2026, 11, 9, 16, 0, tzinfo=TZ),
        ]
        for cron in morning_crons:
            for simulated_time in delayed_times:
                with self.subTest(cron=cron, time=simulated_time.strftime("%H:%M")):
                    session = dispatch_runner.resolve_effective_session(
                        requested_session="auto",
                        now=simulated_time,
                        cron_expr=cron,
                    )
                    self.assertEqual(
                        session,
                        "morning",
                        f"Cron '{cron}' at time {simulated_time} must resolve to 'morning', got '{session}'",
                    )

    def test_staggered_afternoon_crons_resolve_to_afternoon_even_when_delayed(self):
        """Afternoon crons must resolve to 'afternoon' regardless of execution hour."""
        afternoon_crons = [
            "45 5 * * *",
            "50 5 * * *",
            "55 5 * * *",
            "58 5 * * *",
            "0 6 * * *",
            "5 6 * * *",
            "10 6 * * *",
            "20 6 * * *",
            "30 6 * * *",
            "0 7 * * *",
        ]
        delayed_times = [
            datetime(2026, 11, 9, 14, 0, tzinfo=TZ),
            datetime(2026, 11, 9, 15, 30, tzinfo=TZ),
            datetime(2026, 11, 9, 18, 0, tzinfo=TZ),
            datetime(2026, 11, 9, 21, 30, tzinfo=TZ),
        ]
        for cron in afternoon_crons:
            for simulated_time in delayed_times:
                with self.subTest(cron=cron, time=simulated_time.strftime("%H:%M")):
                    session = dispatch_runner.resolve_effective_session(
                        requested_session="auto",
                        now=simulated_time,
                        cron_expr=cron,
                    )
                    self.assertEqual(
                        session,
                        "afternoon",
                        f"Cron '{cron}' at time {simulated_time} must resolve to 'afternoon', got '{session}'",
                    )

    def test_explicit_requested_session_overrides_cron(self):
        """Manual or workflow_dispatch session input overrides cron schedule."""
        now = datetime(2026, 11, 9, 14, 0, tzinfo=TZ)
        # Explicit morning should win even if cron is afternoon
        session_m = dispatch_runner.resolve_effective_session(
            requested_session="morning",
            now=now,
            cron_expr="0 6 * * *",
        )
        self.assertEqual(session_m, "morning")

        # Explicit afternoon should win even if cron is morning
        session_a = dispatch_runner.resolve_effective_session(
            requested_session="afternoon",
            now=now,
            cron_expr="0 0 * * *",
        )
        self.assertEqual(session_a, "afternoon")

    def test_fallback_by_time_when_no_cron(self):
        """When cron is empty and session is auto, fallback to Taipei hour."""
        morning_time = datetime(2026, 11, 9, 9, 15, tzinfo=TZ)
        afternoon_time = datetime(2026, 11, 9, 15, 45, tzinfo=TZ)

        self.assertEqual(
            dispatch_runner.resolve_effective_session("auto", now=morning_time, cron_expr=None),
            "morning",
        )
        self.assertEqual(
            dispatch_runner.resolve_effective_session("auto", now=afternoon_time, cron_expr=""),
            "afternoon",
        )

    def test_staggered_concurrent_runs_prevent_duplicate_dispatch(self):
        """Simulate 3 staggered runs at 07:55, 08:00, 08:05.

        Only the first should send. Subsequent ones must cleanly skip.
        """
        sent_marker = {"sent": False, "claimed": False}

        def mock_check(token, today, session):
            return sent_marker["sent"]

        def mock_claim(token, today, session):
            if sent_marker["claimed"] or sent_marker["sent"]:
                return False
            sent_marker["claimed"] = True
            return True

        def mock_mark(token, today, session):
            sent_marker["sent"] = True

        with patch("dispatch_runner.get_credentials", return_value=("fake_token", "fake_chat_id")), \
             patch("dispatch_runner.check_already_sent_today", side_effect=mock_check), \
             patch("dispatch_runner.claim_session_today", side_effect=mock_claim), \
             patch("dispatch_runner.mark_session_sent_today", side_effect=mock_mark), \
             patch("dispatch_runner.dispatch_report", return_value=True) as mock_dispatch:

            # 1st staggered run (e.g. 07:55) -> should succeed and send
            res1 = dispatch_runner.run_dispatch(session="morning", target_day=None, dry_run=False, force=False)
            self.assertTrue(res1)
            self.assertEqual(mock_dispatch.call_count, 1)

            # 2nd staggered run (e.g. 08:00) -> should be skipped by deduplication guard
            res2 = dispatch_runner.run_dispatch(session="morning", target_day=None, dry_run=False, force=False)
            self.assertTrue(res2)
            # Dispatch must NOT be called again
            self.assertEqual(mock_dispatch.call_count, 1)

            # 3rd staggered run (e.g. 08:05) -> should also be skipped
            res3 = dispatch_runner.run_dispatch(session="morning", target_day=None, dry_run=False, force=False)
            self.assertTrue(res3)
            self.assertEqual(mock_dispatch.call_count, 1)


if __name__ == "__main__":
    unittest.main()
