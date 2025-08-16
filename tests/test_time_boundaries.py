import pytest
from datetime import datetime, timedelta
from freezegun import freeze_time
import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.booking_system import TurfBooking, SlotUnavailableError


@freeze_time("2025-01-01 06:00:00")
def test_booking_cross_midnight():
    turf = TurfBooking(slot_minutes=30)
    late = datetime(2025, 1, 1, 23, 30)
    assert turf.is_slot_available(late) is True


@freeze_time("2025-01-01 06:00:00")
def test_back_to_back_cross_midnight():
    turf = TurfBooking(slot_minutes=30)
    slot1 = datetime(2025, 1, 1, 23, 30)
    slot2 = datetime(2025, 1, 2, 0, 0)
    turf.book_slot(slot1)
    assert turf.is_slot_available(slot2) is True


@freeze_time("2025-01-01 06:00:00")
def test_exact_boundary_overlap():
    turf = TurfBooking(slot_minutes=30)
    s1 = datetime(2025, 1, 1, 8, 0)
    s2 = datetime(2025, 1, 1, 8, 29, 59)
    turf.book_slot(s1)
    with pytest.raises(SlotUnavailableError):
        turf.is_slot_available(s2)
