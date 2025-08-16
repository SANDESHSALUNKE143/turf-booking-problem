import pytest
from datetime import datetime, timedelta
from freezegun import freeze_time
import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.booking_system import TurfBooking


@freeze_time("2025-01-01 00:00:00")
def test_many_sequential_bookings():
    turf = TurfBooking(slot_minutes=30)
    for i in range(0, 24 * 2):
        start = datetime(2025, 1, 1) + timedelta(minutes=30 * i)
        turf.book_slot(start)
    assert len(turf.get_bookings()) == 48


@freeze_time("2025-01-01 06:00:00")
def test_large_slot_duration():
    turf = TurfBooking(slot_minutes=480)
    start = datetime(2025, 1, 1, 8, 0)
    booked_start, booked_end = turf.book_slot(start)
    assert booked_end == datetime(2025, 1, 1, 16, 0)
