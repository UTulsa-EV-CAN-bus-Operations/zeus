from textual import on
from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import Label
from zeus.messages.messages import CANMessageReceived  # Import the event
from textual.app import App

class HMIView(Container):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.status_label = Label("Testing", id="status_label")
        
        self.update_status("System Initialized")

    def update_status(self, message: str) -> None:
        """Update the status label with new information."""
        self.status_label.update(message)

    def compose(self) -> ComposeResult:
        """Render the HMI components."""
        yield self.status_label

    # Handling CAN messages and updating the UI based on CAN IDs
    @on(CANMessageReceived)
    def on_can_message_received(self, event: CANMessageReceived) -> None:
        frame = event.frame
        # Process CAN frame and update status based on conditions
        if frame.can_id == 0x123:  # Example CAN ID
            self.update_status(f"Special message received: {frame.data}")
        elif frame.can_id == 0x456:  # Another example CAN ID
            self.update_status("Important system alert received!")
        else:
            # Default message for other frames
            self.update_status(f"Message from CAN ID {frame.can_id}: {frame.data}")