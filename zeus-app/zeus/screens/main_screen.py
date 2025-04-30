from textual import on
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Footer, Header, Static, TabbedContent, TabPane

from zeus.config.app_config import Settings, TabType
from zeus.views.hmi_view import HMIView
#from zeus.views.live_view import LiveView
from zeus.views.bus_view import BusView
from zeus.views.dbc_view import DBCView
from zeus.views.replay_view import ReplayView


class MainScreen(Screen):
    # The main screen
    
    CSS_PATH = "main_screen.tcss"

    tabbed_content: TabbedContent
    #live_view: LiveView
    hmi_view: HMIView
    bus_view: BusView
    dbc_view: DBCView
    replay_view: ReplayView

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        #self.live_view = LiveView(id="live_view")
        self.hmi_view = HMIView(id="hmi_view")
        self.bus_view = BusView(id="bus_view")
        self.dbc_view = DBCView(id="dbc_view")
        self.replay_view = ReplayView(id="replay_view")

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

            with TabPane("Bus Setup/Info", id="Bus"):
                yield self.bus_view
            with TabPane("DBC Management", id="DBC"):
                yield self.dbc_view
            with TabPane("Replay", id="Replay"):
                yield self.replay_view
            #with TabPane("Live", id="Live"):
            #    yield self.live_view
            with TabPane("HMI", id="HMI"):
                yield self.hmi_view

    
    @on(TabbedContent.TabActivated)
    def on_tab_activated(self) -> None:
        """Tab activated"""
    
    def change_tab(self, tab) -> None:
        self.tabbed_content.active = tab
    