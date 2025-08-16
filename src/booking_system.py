from datetime import datetime, timedelta
from typing import List, Tuple
import logging

# Configure logging for enterprise-level debugging
logger = logging.getLogger(__name__)


class SlotUnavailableError(Exception):
    """Raised when a slot is already booked."""

    def __init__(
        self, message: str, conflicting_slots: List[Tuple[datetime, datetime]] = None
    ):
        super().__init__(message)
        self.conflicting_slots = conflicting_slots or []


class BookingInPastError(Exception):
    """Raised when trying to book a slot in the past."""

    def __init__(self, message: str, requested_time: datetime, current_time: datetime):
        super().__init__(message)
        self.requested_time = requested_time
        self.current_time = current_time


class InvalidSlotDurationError(Exception):
    """Raised when slot duration is invalid."""

    pass


class InvalidSlotRequestError(Exception):
    """Raised when the requested slot input is invalid (e.g., not a datetime object)."""

    def __init__(self, message: str, invalid_value=None):
        super().__init__(message)
        self.invalid_value = invalid_value


class TurfBooking:
    def __init__(self, slot_minutes=30):
        """
        Initialize the turf booking system.

        Args:
            slot_minutes: Duration of each slot in minutes (must be positive)

        Raises:
            InvalidSlotDurationError: If slot_minutes is not positive
        """

        if not isinstance(slot_minutes, int) or slot_minutes <= 0:
            raise InvalidSlotDurationError(
                f"Slot duration must be a positive integer, got: {slot_minutes}"
            )

        self.slot_minutes = slot_minutes
        self.booked_slots: List[Tuple[datetime, datetime]] = []

        logger.info(f"Initialized TurfBooking with {slot_minutes} minute slots")

    def _get_current_time(self) -> datetime:
        """
        Get current time. Separated for easier testing and potential timezone handling.

        Returns:
            Current datetime
        """
        return datetime.now()

    def _find_conflicting_slots(
        self, requested_start: datetime, requested_end: datetime
    ) -> List[Tuple[datetime, datetime]]:
        """
        Find all slots that conflict with the requested time range.

        Args:
            requested_start: Start time of requested slot
            requested_end: End time of requested slot

        Returns:
            List of conflicting slots
        """
        conflicting = []
        for start, end in self.booked_slots:
            # Two intervals overlap if: start1 < end2 and start2 < end1
            if start < requested_end and requested_start < end:
                conflicting.append((start, end))
        return conflicting

    def is_slot_available(self, requested_start: datetime) -> bool:
        """
        Check if the requested slot is available (no overlap).

        Args:
            requested_start: Start time of the requested slot

        Returns:
            True if slot is available

        Raises:
            SlotUnavailableError: If slot conflicts with existing bookings
            TypeError: If requested_start is not a datetime object
        """

        if not isinstance(requested_start, datetime):
            raise InvalidSlotRequestError(
                f"requested_start must be a datetime object, got: {type(requested_start)}",
                invalid_value=requested_start,
            )

        requested_end = requested_start + timedelta(minutes=self.slot_minutes)

        conflicting_slots = self._find_conflicting_slots(requested_start, requested_end)

        if conflicting_slots:
            conflict_details = ", ".join(
                [f"({start} to {end})" for start, end in conflicting_slots]
            )
            raise SlotUnavailableError(
                f"Slot from {requested_start} to {requested_end} conflicts with existing bookings: {conflict_details}",
                conflicting_slots,
            )

        logger.debug(f"Slot {requested_start} to {requested_end} is available")
        return True

    def book_slot(self, requested_start: datetime) -> Tuple[datetime, datetime]:
        """
        Book a slot if it is available and not in the past.

        Args:
            requested_start: Start time of the requested slot

        Returns:
            Tuple of (booked_start, booked_end) times

        Raises:
            BookingInPastError: If requested time is in the past
            SlotUnavailableError: If slot is not available
            TypeError: If requested_start is not a datetime object
        """

        if not isinstance(requested_start, datetime):
            raise InvalidSlotRequestError(
                f"requested_start must be a datetime object, got: {type(requested_start)}",
                invalid_value=requested_start,
            )
        current_time = self._get_current_time()

        # Check if booking is in the past
        if requested_start < current_time:
            raise BookingInPastError(
                f"Cannot book a slot in the past: {requested_start} is before current time {current_time}",
                requested_start,
                current_time,
            )

        # Check availability (this will raise SlotUnavailableError if not available)
        self.is_slot_available(requested_start)

        # Book the slot
        requested_end = requested_start + timedelta(minutes=self.slot_minutes)
        self.booked_slots.append((requested_start, requested_end))

        logger.info(
            f"Successfully booked slot: {requested_start} to {requested_end}"
        )
        return requested_start, requested_end

    def get_bookings(self) -> List[Tuple[datetime, datetime]]:
        """
        Return all current bookings sorted by start time.

        Returns:
            List of (start_time, end_time) tuples sorted chronologically
        """
        return sorted(self.booked_slots, key=lambda x: x[0])
