# -*- coding: utf-8 -*-
"""Manual check: sends Day 1 morning file to the configured chat."""
import sys
from dispatch_runner import run_dispatch

if __name__ == "__main__":
    sys.exit(0 if run_dispatch("morning", 1) else 1)
