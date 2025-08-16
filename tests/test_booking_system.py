import pytest
import sys, os
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from booking_system import TurfBooking


from datetime import datetime, timedelta

def test_book_first_slot():
    turf = TurfBooking(slot_minutes=30)
    start = datetime(2025, 1, 1, 7, 0)
    assert turf.book_slot(start) is True