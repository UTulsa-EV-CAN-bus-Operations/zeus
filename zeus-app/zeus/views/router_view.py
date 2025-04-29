import asyncio
import can

from textual import on
from textual.app import ComposeResult
from textual.containers import Container, VerticalScroll, Horizontal, Vertical
from textual.widgets import Label, Static, Checkbox, Button

class RouterView(Container):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ids_seen = set()
        self.selections = {}  # Track checkbox state {id: bool}
        self.reader = None
        self.notifier = None

    def compose(self) -> ComposeResult:
        with Vertical():
            yield Label("Test")
            yield Button("Select All", id="select_all")
            yield Button("Clear", id="clear")
        self.scroll_area = VerticalScroll()
        yield self.scroll_area

