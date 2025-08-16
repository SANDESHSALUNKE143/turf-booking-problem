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


@freeze_time("2025-01-01 06:00:00")
def test_overlapping_multiple_slots():
    turf = TurfBooking(slot_minutes=30)
    s1 = datetime(2025, 1, 1, 7, 0)
    s2 = datetime(2025, 1, 1, 7, 30)
    turf.book_slot(s1)
    turf.book_slot(s2)
    overlap = datetime(2025, 1, 1, 7, 15)  # overlaps both s1 and s2
    with pytest.raises(SlotUnavailableError):
        turf.is_slot_available(overlap)


@freeze_time("2025-01-01 06:00:00")
def test_back_to_back_cross_midnight():
    turf = TurfBooking(slot_minutes=30)
    slot1 = datetime(2025, 1, 1, 23, 30)
    slot2 = datetime(2025, 1, 2, 0, 0)
    turf.book_slot(slot1)
    assert turf.is_slot_available(slot2) is True


@freeze_time("2025-01-01 06:00:00")
def test_booking_at_now():
    turf = TurfBooking(slot_minutes=30)
    now = datetime.now()
    turf.book_slot(now)
    assert turf.get_bookings()[0][0] == now

@freeze_time("2025-01-01 00:00:00")
def test_many_sequential_bookings():
    turf = TurfBooking(slot_minutes=30)
    for i in range(0, 24*2):  # 48 half-hour slots in a day
        start = datetime(2025, 1, 1) + timedelta(minutes=30*i)
        turf.book_slot(start)
    assert len(turf.get_bookings()) == 48


@freeze_time("2025-01-01 06:00:00")
def test_booking_one_second_in_past():
    """Test booking just one second in the past"""
    turf = TurfBooking(slot_minutes=30)
    past_time = datetime(2025, 1, 1, 5, 59, 59)  # 1 second before current time
    with pytest.raises(BookingInPastError):
        turf.book_slot(past_time)


@freeze_time("2025-01-01 06:00:00")
def test_edge_case_booking_exactly_at_current_time():
    """Test booking at the exact current frozen time"""
    turf = TurfBooking(slot_minutes=30)
    current_time = datetime(2025, 1, 1, 6, 0)  # Same as frozen time
    booked_start, booked_end = turf.book_slot(current_time)
    assert booked_start == current_time
    assert len(turf.get_bookings()) == 1


@freeze_time("2025-01-01 06:00:00")
def test_different_slot_durations():
    """Test the system with different slot durations"""
    # 15-minute slots
    turf_15 = TurfBooking(slot_minutes=15)
    start = datetime(2025, 1, 2, 8, 0)
    booked_start, booked_end = turf_15.book_slot(start)
    assert booked_end == start + timedelta(minutes=15)
    
    # 60-minute slots
    turf_60 = TurfBooking(slot_minutes=60)
    booked_start, booked_end = turf_60.book_slot(start)
    assert booked_end == start + timedelta(minutes=60)


@freeze_time("2025-01-01 06:00:00")
def test_booking_sorted_order():
    """Test that bookings are returned in chronological order"""
    turf = TurfBooking(slot_minutes=30)
    # Book slots out of order
    s3 = datetime(2025, 1, 1, 9, 0)
    s1 = datetime(2025, 1, 1, 7, 0)
    s2 = datetime(2025, 1, 1, 8, 0)
    
    turf.book_slot(s3)
    turf.book_slot(s1) 
    turf.book_slot(s2)
    
    bookings = turf.get_bookings()
    assert bookings[0][0] == s1
    assert bookings[1][0] == s2
    assert bookings[2][0] == s3

@freeze_time("2025-01-01 06:00:00")
def test_exact_boundary_overlap():
    """Test overlaps at exact boundaries - edge case testing"""
    turf = TurfBooking(slot_minutes=30)
    s1 = datetime(2025, 1, 1, 8, 0)  # 8:00-8:30
    s2 = datetime(2025, 1, 1, 8, 29, 59)  # 8:29:59-8:59:59 (overlaps by 1 second)
    
    turf.book_slot(s1)
    with pytest.raises(SlotUnavailableError):
        turf.is_slot_available(s2)


@freeze_time("2025-01-01 06:00:00") 
def test_microsecond_precision():
    """Test handling of microseconds in datetime objects"""
    turf = TurfBooking(slot_minutes=30)
    start_with_microseconds = datetime(2025, 1, 1, 8, 0, 0, 123456)
    booked_start, booked_end = turf.book_slot(start_with_microseconds)
    assert booked_start.microsecond == 123456


def test_empty_system_state():
    """Test initial state of the system"""
    turf = TurfBooking(slot_minutes=30)
    assert len(turf.get_bookings()) == 0
    
    # Any future slot should be available initially
    future_slot = datetime.now() + timedelta(hours=1)
    assert turf.is_slot_available(future_slot) is True

@freeze_time("2025-01-01 06:00:00")
def test_large_slot_duration():
    """Test with unusually large slot durations"""
    turf = TurfBooking(slot_minutes=480)  # 8 hours
    start = datetime(2025, 1, 1, 8, 0)
    booked_start, booked_end = turf.book_slot(start)
    assert booked_end == datetime(2025, 1, 1, 16, 0)




