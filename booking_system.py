from datetime import datetime, timedelta

class TurfBooking:
    def __init__(self, slot_minutes=30):
        self.slot_minutes = slot_minutes
        self.booked_slots = []

    def book_slot(self, requested_start: datetime):

        if requested_start < datetime.now():
            return False
    
        requested_end = requested_start + timedelta(minutes=self.slot_minutes)
        for start, end in self.booked_slots:
            if start < requested_end and requested_start < end:
                return False
        self.booked_slots.append((requested_start, requested_end))
        return True

    def get_bookings(self):
        return self.booked_slots
