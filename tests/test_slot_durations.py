import pytest
from datetime import datetime, timedelta
from freezegun import freeze_time
import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.booking_system import TurfBooking, InvalidSlotDurationError


@freeze_time("2025-01-01 06:00:00")
def test_different_slot_durations():
    turf_15 = TurfBooking(slot_minutes=15)
    start = datetime(2025, 1, 2, 8, 0)
    _, booked_end = turf_15.book_slot(start)
    assert booked_end == start + timedelta(minutes=15)

    turf_60 = TurfBooking(slot_minutes=60)
    _, booked_end = turf_60.book_slot(start)
    assert booked_end == start + timedelta(minutes=60)


def test_zero_or_negative_slot_duration():
    with pytest.raises(InvalidSlotDurationError):
        TurfBooking(slot_minutes=0)
    with pytest.raises(InvalidSlotDurationError):
        TurfBooking(slot_minutes=-30)
