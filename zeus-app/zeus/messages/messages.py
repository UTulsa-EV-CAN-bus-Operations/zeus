from textual.message import Message
from textual.message_pump import MessagePump
from dataclasses import dataclass

from zeus.utils import TabType

@dataclass
class AppRequest(Message):
    # Request the app to perform some action
    widget: MessagePump

@dataclass
class RegisterForUpdates(Message):
    # Register widget for updates
    widget: MessagePump
    event_names: list[str]

@dataclass
class UnregisterForUpdates(Message):
    # Unregister widget for updates
    widget: MessagePump

@dataclass
class ChangeTab(Message):
    # Change to requested tab

    tab: TabType

@dataclass
class UpdateTabLabel(Message):
    # Update tab label

    tab_id: str
    tab_label: str

@dataclass
class CANFrame():
    # Received CAN frame

    timestamp: str
    can_id: str
    rxtx: str
    length: int
    data: str

class CANMessageReceived(Message):
    def __init__(self, sender, frame: CANFrame):
        super().__init__()
        self.sender = sender
        self.frame = frame

class CAN_HMIMessageReceived(Message):
    def __init__(self, sender, frame: CANFrame):
        super().__init__()
        self.sender = sender
        self.frame = frame