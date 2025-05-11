import can

from textual.containers import Vertical
from textual.widgets import  Static, Label
from zeus.widgets.titled_container import TitledContainer


class BusStats(Static):
    """Widget to display bus stats"""

    DEFAULT_CSS = """
    Vertical {
        height: auto;
    }    
"""

    def __init__(self, id:str, bus: can.Bus, busconfig, **kwargs):
        super().__init__(id=id, **kwargs)
        self.border_title = "CAN Bus Status"
        self.border = True
        self.bus = bus
        self.busconfig = busconfig
    
    def compose(self):
        with TitledContainer(title="CAN Connection"):
            with Vertical():
                self.state_label = Label()
                self.interface_label = Label()
                self.channel_label = Label()
                self.bitrate_label = Label()
                yield self.state_label
                yield self.interface_label
                yield self.channel_label
                yield self.bitrate_label

    def on_mount(self):
        self.update_labels()
    
    def set_bus(self, bus: can.Bus, busconfig):
        self.bus = bus
        self.busconfig = busconfig
        self.update_labels()
    
    def watch_bus(self, bus: can.Bus):
        self.update_labels()

    def update_labels(self):
        if self.bus is None:
            self.state_label.update("State: Disconnected")
            self.interface_label.update("Interface: none")
            self.channel_label.update("Channel: none")
            self.bitrate_label.update("Bitrate: none")
        else:
            self.state_label.update(f"State: {self.bus.state.name}")
            self.interface_label.update(f"Interface: {getattr(self.busconfig, 'interface', 'unknown')}")
            self.channel_label.update(f"Channel: {getattr(self.busconfig, 'channel', 'unknown')}")
            self.bitrate_label.update(f"Bitrate: {getattr(self.busconfig, 'bitrate', 'unknown')}")