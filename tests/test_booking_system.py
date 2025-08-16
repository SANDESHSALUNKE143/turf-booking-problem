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
    # Booking should succeed
    booked_start, booked_end = turf.book_slot(start)
    assert (booked_start, booked_end) == (start, start + timedelta(minutes=30))
    # Slot is no longer available
    with pytest.raises(SlotUnavailableError):
        turf.is_slot_available(start)


@freeze_time("2025-01-01 06:00:00")
def test_overlapping_slot_not_allowed():
    turf = TurfBooking(slot_minutes=30)
    first = datetime(2025, 1, 1, 7, 0)
    turf.book_slot(first)
    
    overlap = datetime(2025, 1, 1, 7, 15)
    # Overlapping slot should raise exception
    with pytest.raises(SlotUnavailableError):
        turf.book_slot(overlap)


@freeze_time("2025-01-01 06:00:00")
def test_booking_in_past():
    turf = TurfBooking(slot_minutes=30)
    past_time = datetime(2024, 12, 31, 23, 0)
    # Past booking should raise exception
    with pytest.raises(BookingInPastError):
        turf.book_slot(past_time)


@freeze_time("2025-01-01 06:00:00")
def test_booking_cross_midnight():
    turf = TurfBooking(slot_minutes=30)
    late = datetime(2025, 1, 1, 23, 30)
    assert turf.is_slot_available(late) is True


@freeze_time("2025-01-01 06:00:00")
def test_multiple_bookings():
    turf = TurfBooking(slot_minutes=30)
    s1 = datetime(2025, 1, 1, 6, 0)
    s2 = datetime(2025, 1, 1, 6, 30)
    s3 = datetime(2025, 1, 1, 7, 0)
    s4 = datetime(2025, 1, 1, 6, 45)

    turf.book_slot(s1)
    turf.book_slot(s2)
    turf.book_slot(s3)
    assert len(turf.get_bookings()) == 3

    # Overlapping dynamic slot
    with pytest.raises(SlotUnavailableError):
        turf.is_slot_available(s4)


@freeze_time("2025-01-01 06:00:00")
def test_double_booking_same_slot():
    turf = TurfBooking(slot_minutes=30)
    start = datetime(2025, 1, 1, 8, 0)
    turf.book_slot(start)
    # Second booking same slot should fail
    with pytest.raises(SlotUnavailableError):
        turf.book_slot(start)


@freeze_time("2025-01-01 06:00:00")
def test_boundary_non_overlap():
    turf = TurfBooking(slot_minutes=30)
    s1 = datetime(2025, 1, 1, 9, 0)
    s2 = datetime(2025, 1, 1, 9, 30)
    turf.book_slot(s1)
    assert len(turf.get_bookings()) == 1
    assert turf.is_slot_available(s2) is True



@freeze_time("2025-01-01 06:00:00")
def test_multiple_bookings_with_dynamic_slots():
    turf = TurfBooking(slot_minutes=30)
    s1 = datetime(2025, 1, 1, 6, 0)
    s2 = datetime(2025, 1, 1, 6, 23)

    turf.book_slot(s1)
    with pytest.raises(SlotUnavailableError):
        turf.is_slot_available(s2)
    assert len(turf.get_bookings()) == 1




@freeze_time("2025-01-01 06:00:00")
def test_booking_ofunalligned_slots():
    turf = TurfBooking(slot_minutes=30)
    s1 = datetime(2025, 1, 1, 6, 0)
    s2 = datetime(2025, 1, 1, 6, 33)

    turf.book_slot(s1)
    assert turf.is_slot_available(s2) is True
