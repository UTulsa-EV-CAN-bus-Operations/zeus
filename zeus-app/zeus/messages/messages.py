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