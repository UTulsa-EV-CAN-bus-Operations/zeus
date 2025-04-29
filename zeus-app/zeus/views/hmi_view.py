from textual import on
from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import Label, Static
from zeus.messages.messages import CANMessageReceived, CAN_HMIMessageReceived  # Import the event
from textual.app import App

from zeus.messages.messages import CANFrame, CANMessageReceived

class ChargingPowerWidget(Static):
    """Widget to display Charging Power."""

    def __init__(self):
        super().__init__()
        self.charging_power = 0

    def update_power(self, value):
        self.charging_power = value
        self.update(f"Charging Power: {self.charging_power} W")


class HMIView(Container):

    can_processor: object
    initial_message: str="Current Power: "
    
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.can_processor = self.app.can_processor

    def compose(self) -> ComposeResult:
        self.charging_widget = ChargingPowerWidget()
        yield self.charging_widget
        #yield Static(id="power", content=self.initial_message)

    def on_mount(self) -> None:
        self.can_processor.set_hmi_view(self)
        self.charging_widget.update("Charging Power: ")

    @on(CAN_HMIMessageReceived)
    def handle_message(self, event: CAN_HMIMessageReceived):
        frame = event.frame
        if (frame.can_id == "2EC"):
            data = bytearray.fromhex(frame.data)
            power = int.from_bytes(data[6:8], byteorder='big')
            self.charging_widget.update_power(power)
        """data = frame.data
        static = self.query_one("#power", Static)
        static.update(frame.can_id)"""

        



