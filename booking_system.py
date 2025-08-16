# turf_booking_system/booking_system.py
from datetime import datetime, timedelta

class TurfBooking:
    def __init__(self, slot_minutes=30):
        self.slot_minutes = slot_minutes
        self.booked_slots = []

    def book_slot(self, start: datetime):
        end = start + timedelta(minutes=self.slot_minutes)
        self.booked_slots.append((start, end))
        return True

    def get_bookings(self):
        return self.booked_slots
