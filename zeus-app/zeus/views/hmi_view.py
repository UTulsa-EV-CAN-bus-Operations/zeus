from textual import on
from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import Label, Static

from zeus.messages.messages import CANFrame, CANMessageReceived, CAN_HMIMessageReceived
from zeus.widgets.door_state import DoorState

class HMIView(Container):

    can_processor: object
    initial_message: str="Current Power: "
    
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.can_processor = self.app.can_processor

    def compose(self) -> ComposeResult:
        self.door_widget = DoorState()
        yield self.door_widget
        #yield Static(id="power", content=self.initial_message)

    def on_mount(self) -> None:
        self.can_processor.set_hmi_view(self)
        self.door_widget.update(f"Door State: {self.door_widget.door_state}")

    @on(CAN_HMIMessageReceived)
    def handle_message(self, event: CAN_HMIMessageReceived):
        decoded = event.decoded
        self.door_widget.update_state(decoded)