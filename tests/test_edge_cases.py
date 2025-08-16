import pytest
from datetime import datetime, timedelta
from freezegun import freeze_time
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.booking_system import TurfBooking, SlotUnavailableError

@freeze_time("2025-01-01 06:00:00")
def test_booking_of_unaligned_slots():
    turf = TurfBooking(slot_minutes=30)
    s1 = datetime(2025, 1, 1, 6, 0)
    s2 = datetime(2025, 1, 1, 6, 33)
    turf.book_slot(s1)
    assert turf.is_slot_available(s2) is True

@freeze_time("2025-01-01 06:00:00")
def test_microsecond_precision():
    turf = TurfBooking(slot_minutes=30)
    start_with_microseconds = datetime(2025, 1, 1, 8, 0, 0, 123456)
    booked_start, booked_end = turf.book_slot(start_with_microseconds)
    assert booked_start.microsecond == 123456
