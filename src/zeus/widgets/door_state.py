from textual.widgets import Static

class DoorState(Static):
    """Widget to display if port door is open/closed"""

    def __init__(self):
        super().__init__()
        self.door_state = "Unknown"
    
    def update_state(self, value):
        self.door_state = value
        self.update(f"Door State: {self.door_state}")