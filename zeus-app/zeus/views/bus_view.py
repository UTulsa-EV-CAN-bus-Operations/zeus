import asyncio
import can

from textual import on
from textual import log
from textual.app import ComposeResult
from textual.containers import Container, VerticalScroll, Horizontal, Vertical
from textual.widgets import Label, Static, Checkbox, Button, Select

from zeus.widgets.bus_stats import BusStats
from zeus.widgets.titled_container import TitledContainer

from zeus.config.bus_config import BusConfig, VirtualBusConfig, PCANBusConfig


class BusView(Container):
    
    DEFAULT_CSS = """
    TitledContainer{
        padding: 1;
        border: round white;
        height: auto;
        width: auto;
    }
    Select{
        width: 50;
        border: round rgb(11, 127, 204);
    }
    #bus_setup {
        width: 60;
        height: auto;
        margin: 1
    }
    #bus_stats {
        width: 60;
        height: auto;
    }
    
"""
    
    bus: object
    bus_config: BusConfig 
    bus_select: Select
    bus_stats: BusStats
    bus_connect: Button
    bus_disconnect: Button
    can_processor: object
    


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # CAN Bus Interface Select
        self.bus_select = Select(id="bus_select", prompt="Select CAN Bus Interface", options=[("PCAN","pcan"),("Virtual","virtual")])
        self.bus_select.border_title = "CAN Bus Interface Selection: "
        self.bus_connect = Button(id="bus_connect", label="Connect")
        self.bus_disconnect = Button(id="bus_disconnect", label="Disconnect")
        
        # Wire CAN_Processor
        self.can_processor = self.app.can_processor
        self.bus_config = self.can_processor.bus1config

        self.bus_stats = BusStats(self.can_processor.bus1, self.bus_config)


    def compose(self) -> ComposeResult:
        with TitledContainer("Connect Bus:"):
            with Vertical(id="bus_setup"):
                yield self.bus_select
                with Horizontal(id="bus_setup"):
                    yield self.bus_connect
                    yield self.bus_disconnect
        
        with TitledContainer("Bus Stats: "):
            with Vertical(id="bus_stats"):
                yield self.bus_stats

    @on(Button.Pressed)
    def on_button_press(self, event:Button.Pressed) -> None:
        event.stop()
        ctrl: Button = event.control
        if ctrl.id == "bus_connect":
            self.can_processor.initializeBus(self.busconfig)
            self.bus_stats.set_bus(self.can_processor.bus1,self.can_processor.bus1config)
        elif ctrl.id == "bus_disconnect":
            self.can_processor.bus1.shutdown()
            self.bus_stats.set_bus(None, None)
                
    @on(Select.Changed)
    def on_select_changed(self, event:Select.Changed) -> None:
        event.stop()
        ctrl: Select = event.control

        if ctrl.id == "bus_select":
            if event.value == 'pcan':
                log('pcan selected')
                self.busconfig = PCANBusConfig()
            elif event.value == 'virtual':
                log('virtual selected')
                self.busconfig = VirtualBusConfig()


