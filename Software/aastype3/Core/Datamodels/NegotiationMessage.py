import json

class NegotiationMessage:
    _instance = None
    _initialized = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, free_time_slots: list | None = None, booked_time_slots: list | None = None, requested_slot: str | None = None):
        # Only initialize once
        if self._initialized:
            return        
        self.free_time_slots = free_time_slots
        self.booked_time_slots = booked_time_slots
        self.requested_slot = requested_slot

        self.resource_id = None
        self.time_slot_state = self._check_time_slot_availability()
        self.time_slot_next = self._find_alternative_time_slot()
        self.violations = None
        
        self._initialized = True

    def update(self, free_time_slots: list | None = None, booked_time_slots: list | None = None, requested_slot: str | None = None):
        """Update the singleton instance with new values"""
        if free_time_slots is not None:
            self.free_time_slots = free_time_slots
        if booked_time_slots is not None:
            self.booked_time_slots = booked_time_slots
        if requested_slot is not None:
            self.requested_slot = requested_slot
        self.update_time_slot_info()

    def update_time_slot_info(self):
        self.time_slot_state = self._check_time_slot_availability()
        self.time_slot_next = self._find_alternative_time_slot()

    def create_message_to_publish(self) -> str:
        return json.dumps(
            {
                "resource_id": self.resource_id,
                "time_slot_state": self.time_slot_state,
                "time_slot_next": self.time_slot_next,
                "violations": self.violations,
            }
        )

    def _check_time_slot_availability(self):
        if self.booked_time_slots is None or self.free_time_slots is None or self.requested_slot is None:
            return None
        if self.requested_slot in self.booked_time_slots:
            return "booked"
        elif self.requested_slot in self.free_time_slots:
            return "available"
        else:
            return "unavailable"
      
    def _find_alternative_time_slot(self):
        if self.time_slot_state == "available":
            return self.requested_slot
        
        if not self.free_time_slots:
            return None
        
        if not self.requested_slot:
            return self.free_time_slots[0]
        
        for slot in self.free_time_slots:
            if slot.split("-")[0] > self.requested_slot.split("-")[0]:
                return slot