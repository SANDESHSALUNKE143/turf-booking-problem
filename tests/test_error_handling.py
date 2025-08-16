"""
Error Handling & Validation Tests
Tests that verify proper error conditions and input validation
"""

import pytest
import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.booking_system import (
    TurfBooking,
    SlotUnavailableError,
    BookingInPastError,
    InvalidSlotDurationError,
    InvalidSlotRequestError,
)
from freezegun import freeze_time
from datetime import datetime, timedelta


@freeze_time("2025-01-01 06:00:00")
def test_booking_in_past():
    """Test booking in the past (2024 vs 2025)"""
    turf = TurfBooking(slot_minutes=30)
    past_time = datetime(2024, 12, 31, 23, 0)
    # Past booking should raise exception
    with pytest.raises(BookingInPastError):
        turf.book_slot(past_time)


@freeze_time("2025-01-01 06:00:00")
def test_zero_or_negative_slot_duration():
    """Test invalid slot durations (0, negative)"""
    # Test zero duration
    with pytest.raises(InvalidSlotDurationError) as exc_info:
        turf = TurfBooking(slot_minutes=0)
    assert "positive integer" in str(exc_info.value)

    # Test negative duration
    with pytest.raises(InvalidSlotDurationError) as exc_info:
        turf = TurfBooking(slot_minutes=-30)
    assert "positive integer" in str(exc_info.value)

    # Test non-integer duration
    with pytest.raises(InvalidSlotDurationError):
        turf = TurfBooking(slot_minutes=30.5)


@freeze_time("2025-01-01 06:00:00")
def test_input_validation():
    """Test input validation for various invalid inputs"""
    turf = TurfBooking(slot_minutes=30)

    # Test None input
    with pytest.raises(InvalidSlotRequestError):
        turf.is_slot_available(None)

    with pytest.raises(InvalidSlotRequestError):
        turf.book_slot(None)

    # Test string input
    with pytest.raises(InvalidSlotRequestError):
        turf.is_slot_available("2025-01-01 08:00")

    # Test integer input
    with pytest.raises(InvalidSlotRequestError):
        turf.book_slot(20250101)

    # Test list input
    with pytest.raises(InvalidSlotRequestError):
        turf.book_slot([2025, 1, 1, 8, 0])


@freeze_time("2025-01-01 06:00:00")
def test_exception_details():
    """Test that exceptions contain useful debugging information"""
    turf = TurfBooking(slot_minutes=30)

    # Book a slot first
    first_slot = datetime(2025, 1, 1, 8, 0)
    turf.book_slot(first_slot)

    # Try to book overlapping slot and check exception details
    overlap_slot = datetime(2025, 1, 1, 8, 15)
    with pytest.raises(SlotUnavailableError) as exc_info:
        turf.is_slot_available(overlap_slot)

    # Check that exception contains useful information
    assert "8:15" in str(exc_info.value)
    assert hasattr(exc_info.value, "conflicting_slots")
    assert len(exc_info.value.conflicting_slots) == 1

    # Test BookingInPastError details
    past_time = datetime(2024, 12, 31, 23, 0)
    with pytest.raises(BookingInPastError) as exc_info:
        turf.book_slot(past_time)

    assert hasattr(exc_info.value, "requested_time")
    assert hasattr(exc_info.value, "current_time")
    assert exc_info.value.requested_time == past_time


@freeze_time("2025-01-01 06:00:00")
def test_booking_far_past():
    """Test booking very far in the past"""
    turf = TurfBooking(slot_minutes=30)
    very_old = datetime(2020, 1, 1, 12, 0)
    with pytest.raises(BookingInPastError) as exc_info:
        turf.book_slot(very_old)

    # Check the time difference is captured
    error = exc_info.value
    time_diff = error.current_time - error.requested_time
    assert time_diff.days > 1800  # More than 5 years


@freeze_time("2025-01-01 06:00:00")
def test_error_message_clarity():
    """Test that error messages are clear and actionable"""
    turf = TurfBooking(slot_minutes=30)

    # Test InvalidSlotDurationError message
    with pytest.raises(InvalidSlotDurationError) as exc_info:
        TurfBooking(slot_minutes=0)

    error_msg = str(exc_info.value)
    assert "positive integer" in error_msg
    assert "0" in error_msg

    # Test SlotUnavailableError with conflict details
    turf.book_slot(datetime(2025, 1, 1, 8, 0))
    with pytest.raises(SlotUnavailableError) as exc_info:
        turf.book_slot(datetime(2025, 1, 1, 8, 15))

    error_msg = str(exc_info.value)
    assert "conflicts with existing bookings" in error_msg
    assert "8:00" in error_msg  # Shows conflicting time


def test_datetime_timezone_handling():
    """Test behavior with timezone-aware datetime objects"""
    try:
        import pytz
    except ImportError:
        pytest.skip("pytz not available for timezone testing")

    turf = TurfBooking(slot_minutes=30)

    # Create timezone-aware datetime
    utc = pytz.UTC
    aware_dt = datetime(2025, 1, 2, 8, 0, tzinfo=utc)

    # Test how system handles timezone-aware vs naive datetime
    try:
        booked_start, booked_end = turf.book_slot(aware_dt)
        # If this works, system accepts timezone-aware datetime
        assert booked_start == aware_dt
    except (TypeError, ValueError) as e:
        # System doesn't handle timezone-aware datetime properly
        assert "timezone" in str(e).lower() or "aware" in str(e).lower()


@freeze_time("2025-01-01 06:00:00")
def test_concurrent_booking_simulation():
    """Simulate concurrent booking attempts (race condition testing)"""
    turf = TurfBooking(slot_minutes=30)

    # Simulate two users trying to book the same slot
    slot_time = datetime(2025, 1, 1, 8, 0)

    # First booking succeeds
    turf.book_slot(slot_time)

    # Second booking should fail
    with pytest.raises(SlotUnavailableError):
        turf.book_slot(slot_time)

    # Verify only one booking exists
    assert len(turf.get_bookings()) == 1
