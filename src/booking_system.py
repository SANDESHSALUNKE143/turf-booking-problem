from datetime import datetime, timedelta

class SlotUnavailableError(Exception):
    """Raised when a slot is already booked."""
    pass

class BookingInPastError(Exception):
    """Raised when trying to book a slot in the past."""
    pass

class TurfBooking:
    def __init__(self, slot_minutes=30):
        self.slot_minutes = slot_minutes
        self.booked_slots = []

    def is_slot_available(self, requested_start: datetime):
        """Check if the requested slot is available (no overlap)."""
        requested_end = requested_start + timedelta(minutes=self.slot_minutes)
        for start, end in self.booked_slots:
            if start < requested_end and requested_start < end:
                raise SlotUnavailableError(f"Slot from {requested_start} to {requested_end} is already booked.")
            
        return True

    def book_slot(self, requested_start: datetime):
        """Book a slot if it is available and not in the past."""
        # Reject past bookings
        if requested_start < datetime.now():
            raise BookingInPastError(f"Cannot book a slot in the past: {requested_start}")

        # Check availability
        self.is_slot_available(requested_start)

        # Book the slot
        requested_end = requested_start + timedelta(minutes=self.slot_minutes)
        self.booked_slots.append((requested_start, requested_end))
        return requested_start, requested_end  # Return the booked slot for confirmation

    def get_bookings(self):
        """Return all current bookings sorted by start time."""
        return sorted(self.booked_slots)
