import asyncio
import can

from textual import on
from textual import log
from textual.app import ComposeResult
from textual.containers import Container, VerticalScroll, Horizontal, Vertical
from textual.widgets import Label, Static, Checkbox, Button, Select

from zeus.widgets.bus_stats import BusStats
from zeus.widgets.titled_container import TitledContainer

from zeus.config.bus_config import BusConfig
from zeus.can_processor import CANProcessor


class PassthroughView(Container):
    
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

    bus1: object
    bus1_config: BusConfig 
    bus1_select: Select
    bus1_stats: BusStats
    bus1_connect: Button
    bus1_disconnect: Button

    bus2: object
    bus2_config: BusConfig 
    bus2_select: Select
    bus2_stats: BusStats
    bus2_connect: Button
    bus2_disconnect: Button

    passthrough_Start_Button : Button
    passthrough_Stop_Button : Button

    can_processor: CANProcessor
    

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Get connection to can_processor
        self.can_processor = self.app.can_processor

        # CAN Bus 1 Interface Select
        self.bus1_select = Select(id="bus1_select", prompt="Select CAN Bus 1 Interface", options=[("PCAN","pcan")])
        self.bus1_select.border_title = "CAN Bus 1 Interface Selection: "
        self.bus1_connect = Button(id="bus1_connect", label="Connect")
        self.bus1_disconnect = Button(id="bus1_disconnect", label="Disconnect")
        self.bus1_config = None
        self.bus1_stats = BusStats("bus1", None, None)
        
        # CAN Bus 2 Interface Select
        self.bus2_select = Select(id="bus2_select", prompt="Select CAN Bus 2 Interface", options=[("PCAN","pcan")])
        self.bus2_select.border_title = "CAN Bus 2 Interface Selection: "
        self.bus2_connect = Button(id="bus2_connect", label="Connect")
        self.bus2_disconnect = Button(id="bus2_disconnect", label="Disconnect")
        self.bus2_config = None
        self.bus2_stats = BusStats("bus2", None, None)

        # Setup Buttons for controlling passthrough
        self.passthrough_Start_Button = Button(id = "Start_Passthrough", label= "Start Passthrough")
        self.passthrough_Stop_Button = Button(id = "Stop_Passthrough", label= "Stop Passthrough")

    def compose(self) -> ComposeResult:
        with Horizontal():
            with Vertical():
                with TitledContainer("Connect Bus 1:"):
                    with Vertical(id="bus1_setup"):
                        yield self.bus1_select
                        with Horizontal(id="bus1_setup"):
                            yield self.bus1_connect
                            yield self.bus1_disconnect
                
                with TitledContainer("Bus 1 Stats: "):
                    with Vertical(id="bus1_stats"):
                        yield self.bus1_stats

            with Vertical():
                yield self.passthrough_Start_Button
                yield self.passthrough_Stop_Button

            
            with Vertical():
                with TitledContainer("Connect Bus 2:"):
                    with Vertical(id="bus2_setup"):
                        yield self.bus2_select
                        with Horizontal(id="bus2_setup"):
                            yield self.bus2_connect
                            yield self.bus2_disconnect
                
                with TitledContainer("Bus 2 Stats: "):
                    with Vertical(id="bus2_stats"):
                        yield self.bus2_stats


    @on(Button.Pressed)
    def on_button_press(self, event:Button.Pressed) -> None:
        event.stop()
        ctrl: Button = event.control
    
        if ctrl.id == "bus1_connect":
            if (self.bus1_config!=None):
                self.can_processor.initializeBus(self.bus_config, self.bus1_config.channel)
                self.bus1_stats.set_bus(self.can_processor.busDict[self.bus1_config.channel], self.can_processor.configDict[self.bus1_config.channel])
        elif ctrl.id == "bus1_disconnect":
            self.can_processor.busDict[self.bus1_config.channel].shutdown()
            self.bus1_stats.set_bus(None, None)

        if ctrl.id == "bus2_connect":
            if (self.bus2_config!=None):
                self.can_processor.initializeBus(self.bus_config, self.bus2_config.channel)
                self.bus2_stats.set_bus(self.can_processor.busDict[self.bus2_config.channel], self.can_processor.configDict[self.bus2_config.channel])
        elif ctrl.id == "bus2_disconnect":
            self.can_processor.busDict[self.bus2_config.channel].shutdown()
            self.bus2_stats.set_bus(None, None)

        if ctrl.id == "Start_Passthrough":
            pass # TODO: Implement passthrough scripts
        elif ctrl.id == "Stop_Passthrough":
            pass # TODO: Figure out how to stop passthrough Scripts
                
    @on(Select.Changed)
    def on_select_changed(self, event:Select.Changed) -> None:
        event.stop()
        ctrl: Select = event.control

        if ctrl.id == "bus1_select":
            if event.value == 'pcan':
                log('pcan selected')
                self.bus1_config = BusConfig(interface="pcan", channel="PCAN_USBBUS1", bitrate=500000)

        if ctrl.id == "bus2_select":
            if event.value == 'pcan':
                log('pcan selected')
                self.bus2_config = BusConfig(interface="pcan", channel="PCAN_USBBUS2", bitrate=500000)