from textual import on
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Footer, Header, Static, TabbedContent, TabPane

from zeus.config.app_config import Settings, TabType
from zeus.views.hmi_view import HMIView
from zeus.views.live_view import LiveView


class MainScreen(Screen):
    # The main screen
    
    CSS_PATH = "main_screen.tcss"

    tabbed_content: TabbedContent
    live_view: LiveView
    hmi_view: HMIView

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.live_view = LiveView(id="live_view")
        self.hmi_view = HMIView(id="hmi_view")

    async def on_mount(self) -> None:
        self.set_timer(0.5, self.done_loading)
    
    def done_loading(self) -> None:
        self.tabbed_content.loading = False

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Footer()
        
        with TabbedContent(
            id="tabbed_content",
            initial=Settings.startTab,
        ) as tc:
            self.tabbed_content = tc
            tc.loading = True

            with TabPane("Live", id="Live"):
                yield self.live_view
            with TabPane("HMI", id="HMI"):
                yield self.hmi_view

    
    @on(TabbedContent.TabActivated)
    def on_tab_activated(self) -> None:
        """Tab activated"""
    
    def change_tab(self, tab) -> None:
        self.tabbed_content.active = tab
    