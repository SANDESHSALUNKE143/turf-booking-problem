import pytest
from datetime import datetime, timedelta
from freezegun import freeze_time
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.booking_system import TurfBooking, SlotUnavailableError

@freeze_time("2025-01-01 06:00:00")
def test_overlapping_slot_not_allowed():
    turf = TurfBooking(slot_minutes=30)
    first = datetime(2025, 1, 1, 7, 0)
    turf.book_slot(first)
    overlap = datetime(2025, 1, 1, 7, 15)
    with pytest.raises(SlotUnavailableError):
        turf.book_slot(overlap)

@freeze_time("2025-01-01 06:00:00")
def test_double_booking_same_slot():
    turf = TurfBooking(slot_minutes=30)
    start = datetime(2025, 1, 1, 8, 0)
    turf.book_slot(start)
    with pytest.raises(SlotUnavailableError):
        turf.book_slot(start)

@freeze_time("2025-01-01 06:00:00")
def test_overlapping_multiple_slots():
    turf = TurfBooking(slot_minutes=30)
    s1 = datetime(2025, 1, 1, 7, 0)
    s2 = datetime(2025, 1, 1, 7, 30)
    turf.book_slot(s1)
    turf.book_slot(s2)
    overlap = datetime(2025, 1, 1, 7, 15)
    with pytest.raises(SlotUnavailableError):
        turf.is_slot_available(overlap)
