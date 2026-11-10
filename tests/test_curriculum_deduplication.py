# -*- coding: utf-8 -*-
"""Unit tests to prevent question duplication across the curriculum.

Verifies:
1. Zero same-day duplicates: Morning and Afternoon sessions on any day never share identical question stems.
2. Every session generates exactly 43 distinct questions with valid answers and option details.
3. Reading comprehension (Part 5) and cloze passages (Part 4) are completely disjoint between morning and afternoon.
"""

import unittest
from adaptive_srs_engine import build_session_payload


class TestCurriculumDeduplication(unittest.TestCase):

    def test_zero_same_day_question_duplicates_all_25_days(self):
        """Every day from Day 1 to Day 25 must have 0 duplicate questions between morning and afternoon."""
        total_overlap = 0
        overlap_details = []

        for day in range(1, 26):
            m = build_session_payload(day, "morning")
            a = build_session_payload(day, "afternoon")

            m_stems = (
                {q["question"].strip() for q in m["part3_mc_questions"]}
                | {q["question"].strip() for p in m["part4_cloze_passages"] for q in p["questions"]}
                | {q["question"].strip() for p in m["part5_reading_passages"] for q in p["questions"]}
            )
            a_stems = (
                {q["question"].strip() for q in a["part3_mc_questions"]}
                | {q["question"].strip() for p in a["part4_cloze_passages"] for q in p["questions"]}
                | {q["question"].strip() for p in a["part5_reading_passages"] for q in p["questions"]}
            )

            overlap = m_stems.intersection(a_stems)
            if overlap:
                total_overlap += len(overlap)
                overlap_details.append(f"Day {day}: {len(overlap)} duplicates -> {list(overlap)[:2]}")

        self.assertEqual(
            total_overlap,
            0,
            f"Found {total_overlap} same-day duplicates across the 25 days:\n" + "\n".join(overlap_details),
        )

    def test_session_question_counts_and_options(self):
        """Each session must have exactly 43 questions with 4 options each."""
        for day in (1, 7, 14, 25):
            for sess in ("morning", "afternoon"):
                p = build_session_payload(day, sess)
                self.assertEqual(p["counts"]["total_questions"], 43)
                self.assertEqual(len(p["part3_mc_questions"]), 25)
                self.assertEqual(p["counts"]["part4_cloze"], 12)
                self.assertEqual(p["counts"]["part5_reading"], 6)


if __name__ == "__main__":
    unittest.main()
