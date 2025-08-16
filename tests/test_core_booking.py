import pytest
import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.booking_system import TurfBooking, SlotUnavailableError, BookingInPastError
from freezegun import freeze_time
from datetime import datetime, timedelta


@freeze_time("2025-01-01 06:00:00")
def test_book_first_slot():
    turf = TurfBooking(slot_minutes=30)
    start = datetime(2025, 1, 1, 7, 0)
    booked_start, booked_end = turf.book_slot(start)
    assert (booked_start, booked_end) == (start, start + timedelta(minutes=30))
    with pytest.raises(SlotUnavailableError):
        turf.is_slot_available(start)


@freeze_time("2025-01-01 06:00:00")
def test_booking_in_past():
    turf = TurfBooking(slot_minutes=30)
    past_time = datetime(2024, 12, 31, 23, 0)
    with pytest.raises(BookingInPastError):
        turf.book_slot(past_time)


@freeze_time("2025-01-01 06:00:00")
def test_booking_at_now():
    turf = TurfBooking(slot_minutes=30)
    now = datetime.now()
    turf.book_slot(now)
    assert turf.get_bookings()[0][0] == now


@freeze_time("2025-01-01 06:00:00")
def test_empty_system_state():
    turf = TurfBooking(slot_minutes=30)
    assert len(turf.get_bookings()) == 0
    future_slot = datetime.now() + timedelta(hours=1)
    assert turf.is_slot_available(future_slot) is True
