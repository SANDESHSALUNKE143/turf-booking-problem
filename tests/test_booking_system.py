import pytest
import sys, os
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from booking_system import TurfBooking
from freezegun import freeze_time


from datetime import datetime, timedelta


@freeze_time("2025-01-01 06:00:00")
def test_book_first_slot():
    turf = TurfBooking(slot_minutes=30)
    start = datetime(2025, 1, 1, 7, 0)
    assert turf.book_slot(start) is True

@freeze_time("2025-01-01 06:00:00")
def test_overlapping_slot_not_allowed():
    turf = TurfBooking(slot_minutes=30)
    first = datetime(2025, 1, 1, 7, 0)
    turf.book_slot(first)
    
    overlap = datetime(2025, 1, 1, 7, 15)
    assert turf.book_slot(overlap) is False

@freeze_time("2025-01-01 06:00:00")
def test_booking_in_past():
    turf = TurfBooking(slot_minutes=30)
    past_time = datetime(2024, 12, 31, 23, 0)
    assert turf.book_slot(past_time) is False


@freeze_time("2025-01-01 06:00:00")
def test_booking_cross_midnight():
    turf = TurfBooking(slot_minutes=30)
    late = datetime(2025, 1, 1, 23, 30)
    assert turf.book_slot(late) is True
    assert turf.get_bookings()[0][1] == datetime(2025, 1, 2, 0, 0)
