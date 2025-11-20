import json
from datetime import datetime, timedelta
from typing import List

class TimeSlotDataType:
    def __init__(self, start_time: str = "08:00", end_time: str = "17:00", duration_minutes: int = 20):
        self.start_time = start_time  # Expected format "HH:MM"
        self.end_time = end_time      # Expected format "HH:MM"
        self.duration_minutes = duration_minutes  # Duration in minutes
        self.free_slots = []  # List of available time slots
        self.booked_slots = []  # List of booked/allocated time slots
    
    def __repr__(self):
        return f"TimeSlotDataType(start={self.start_time}, end={self.end_time}, duration={self.duration_minutes}min, free={len(self.free_slots)}, booked={len(self.booked_slots)})"
    def get_duration_minutes(self) -> int:
        return self.duration_minutes
    def to_dict(self) -> dict:
        return {
            "start_time": self.start_time,
            "end_time": self.end_time,
            "duration_minutes": self.duration_minutes,
            "free_slots": self.free_slots,
            "booked_slots": self.booked_slots
        }
    
    def to_json(self) -> str:
        """Convert to JSON string for AAS storage."""
        return json.dumps(self.to_dict())
    
    def get_booked_slots_json(self) -> str:
        """Get booked slots as separate JSON string."""
        return json.dumps(self.booked_slots)
    
    def get_free_slots_json(self) -> str:
        """Get free slots as separate JSON string."""
        return json.dumps(self.free_slots)
    def get_booked_slots_csv(self, sep=",") -> str:
        """Booked slots as CSV (no [] brackets)."""
        return sep.join(self.booked_slots)
    def get_free_slots_csv(self, sep=",") -> str:
        """Free slots as CSV (no [] brackets)."""
        return sep.join(self.free_slots)
    
    @classmethod
    def from_dict(cls, data: dict):
        obj = cls(
            start_time=data.get("start_time", "08:00"),
            end_time=data.get("end_time", "17:00"),
            duration_minutes=data.get("duration_minutes", 20)
        )
        obj.free_slots = data.get("free_slots", [])
        obj.booked_slots = data.get("booked_slots", [])
        return obj
    
    @classmethod
    def from_dict(cls, data: dict):
        obj = cls(
            start_time=data.get("start_time", "08:00"),
            end_time=data.get("end_time", "17:00"),
            duration_minutes=data.get("duration_minutes", 20)
        )
        # Make sure you're only setting booked slots from the data, not all slots
        obj.free_slots = data.get("free_slots", [])
        obj.booked_slots = data.get("booked_slots", [])  # Should only have actually booked slots
        return obj
        
    def get_free_slots(self) -> List[str]:
        """
        Generate all free time slots between start and end time.
        
        Returns:
            List of slot strings like ["08:00-08:20", "08:20-08:40", ...]
        """
        slots = []
        
        # Parse start and end times
        start_dt = datetime.strptime(self.start_time, "%H:%M")
        end_dt = datetime.strptime(self.end_time, "%H:%M")
        
        current = start_dt
        while current + timedelta(minutes=self.duration_minutes) <= end_dt:
            slot_start = current.strftime("%H:%M")
            slot_end = (current + timedelta(minutes=self.duration_minutes)).strftime("%H:%M")
            slots.append(f"{slot_start}-{slot_end}")
            current += timedelta(minutes=self.duration_minutes)
        
        self.free_slots = slots
        return slots
    
    def is_slot_available(self, time_slot: str) -> bool:
        """
        Check if a time slot is available (not booked).
        
        Args:
            time_slot: slot string like "08:00-08:20"
        
        Returns:
            True if slot is in free_slots and not in booked_slots
        """
        return time_slot in self.free_slots and time_slot not in self.booked_slots
    
    def allocate_slot(self, time_slot: str) -> bool:
        """
        Allocate (book) a slot from available slots.
        
        Args:
            time_slot: slot string to allocate
        
        Returns:
            True if successfully allocated, False if already taken
        """
        if self.is_slot_available(time_slot):
            self.free_slots.remove(time_slot)
            self.booked_slots.append(time_slot)
            self.booked_slots.sort()
            return True
        return False
    
    def release_slot(self, time_slot: str) -> bool:
        """
        Release (cancel booking) a slot back to available slots.
        
        Args:
            time_slot: slot string to release
        
        Returns:
            True if successfully released, False if not booked
        """
        if time_slot in self.booked_slots:
            self.booked_slots.remove(time_slot)
            self.free_slots.append(time_slot)
            self.free_slots.sort()
            return True
        return False
    
    def get_all_slots(self) -> dict:
        """Get all slots (free and booked) as a dict."""
        return {
            "free": self.free_slots,
            "booked": self.booked_slots,
            "total": len(self.free_slots) + len(self.booked_slots)
        }


""" # Usage example
if __name__ == "__main__":
    # Create time slot manager
    ts = TimeSlotDataType(start_time="08:00", end_time="12:00", duration_minutes=30)
    
    # Generate all free slots
    slots = ts.get_free_slots()
    print(f"All slots: {slots}")
    # Output: ['08:00-08:30', '08:30-09:00', '09:00-09:30', ...]
    
    # Convert to JSON for AAS storage
    json_str = ts.to_json()
    print(f"Full JSON: {json_str}")
    
    # Allocate slots
    ts.allocate_slot("08:00-08:30")
    ts.allocate_slot("09:00-09:30")
    print(f"\nFree slots: {ts.free_slots}")
    print(f"Booked slots: {ts.booked_slots}")
    
    # Get separate JSON strings
    free_json = ts.get_free_slots_json()
    booked_json = ts.get_booked_slots_json()
    print(f"\nFree slots JSON: {free_json}")
    print(f"Booked slots JSON: {booked_json}")
    
    # View all slots
    all_slots = ts.get_all_slots()
    print(f"\nAll slots summary: {all_slots}")
    
    # Release a slot
    ts.release_slot("08:00-08:30")
    print(f"\nAfter release:")
    print(f"Free slots: {ts.free_slots}")
    print(f"Booked slots: {ts.booked_slots}")
    
    # Recreate from JSON
    ts2 = TimeSlotDataType.from_json(json_str)
    print(f"\nRestored from JSON: {ts2}") """