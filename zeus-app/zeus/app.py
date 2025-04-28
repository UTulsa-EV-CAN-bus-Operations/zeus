from textual import on, work
from textual.app import App
from textual.binding import Binding
from textual.color import Color
from textual.widget import Widget
from textual.widgets import Input, Select, TextArea

from zeus.screens.main_screen import MainScreen
from zeus.messages.messages import (
    AppRequest, 
    ChangeTab, 
    RegisterForUpdates, 
    UnregisterForUpdates, 
    UpdateTabLabel,
    )

class ZeusAnalysis(App):
    TITLE = "Zeus"
    BINDINGS = [
        Binding(key="q", action="quit",description="Quit")
    ]

    main_screen: MainScreen

    def __init__(self) -> None:
        super().__init__()
    
    async def on_mount(self) -> None:
        """Display screen."""
        self.main_screen = MainScreen()

        await self.push_screen(self.main_screen)
    
    @on(ChangeTab)
    def on_change_tab(self, event: ChangeTab) -> None:
        event.stop()
        self.main_screen.change_tab(event.tab)