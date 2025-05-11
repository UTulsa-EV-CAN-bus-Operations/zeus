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

from usbmonitor import USBMonitor
from usbmonitor.attributes import ID_MODEL, ID_MODEL_ID, ID_VENDOR_ID


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
    bus_setup_select: Select
    bus_teardown_select: Select
    bus_stats: BusStats
    bus_connect: Button
    bus_disconnect: Button
    can_processor: CANProcessor
    USBList: list[(str, str)]
    SetupSelectList: list[(str, str)]
    toTeardown: str

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Wire CAN_Processor
        self.can_processor = self.app.can_processor
        self.bus_config = None

        # CAN Bus Interface Select
        self.SetupSelectList = []
        self.USBMonitor = USBMonitor()
        self.updateSelectList()

        self.TeardownSelectList = [("None", "none")]
        
        self.bus_setup_select = Select(id="bus_setup_select", prompt="Select CAN Bus Interface", options=self.SetupSelectList)

        self.bus_teardown_select = Select(id="bus_teardown_select", prompt="Select Active CAN Bus Interface", options=self.TeardownSelectList)
        
        self.bus_setup_select.border_title = "CAN Bus Interface Selection: "
        self.bus_connect = Button(id="bus_connect", label="Connect")
        self.bus_disconnect = Button(id="bus_disconnect", label="Disconnect")

        self.toTeardown = None

        self.bus_stats = BusStats("recentlyAdded",None,None)

    def compose(self) -> ComposeResult:
        with Horizontal():
            with Vertical():
                with TitledContainer("Connect Bus:"):
                            with Vertical(id="bus_setup"):
                                yield self.bus_setup_select
                                with Horizontal(id="bus_setup"):
                                    yield self.bus_connect
                            with Vertical(id="bus_teardown"):
                                yield self.bus_teardown_select
                                with Horizontal(id="bus_teardown"):
                                    yield self.bus_disconnect

                with TitledContainer("Bus Stats: "):
                    with Vertical(id="bus_stats"):
                        yield self.bus_stats

            yield VerticalScroll(id="CAN_connections")

    @on(Button.Pressed)
    def on_button_press(self, event:Button.Pressed) -> None:
        event.stop()
        ctrl: Button = event.control
    
        if ctrl.id == "bus_connect":
            if (self.bus_config!=None):
                self.can_processor.initializeBus(self.bus_config, self.bus_config.channel) # Meow
                self.bus_stats.set_bus(self.can_processor.busDict[self.bus_config.channel],self.can_processor.configDict[self.bus_config.channel])
                
                new_CAN_Connection = BusStats(self.bus_config.channel, bus = self.can_processor.busDict[self.bus_config.channel], busconfig = self.can_processor.configDict[self.bus_config.channel])
                self.query_one("#CAN_connections").mount(new_CAN_Connection)
                new_CAN_Connection.scroll_visible()
                

                self.TeardownSelectList = []
                for key in self.can_processor.configDict.keys():
                    self.TeardownSelectList.append((self.can_processor.configDict[key].channel, self.can_processor.configDict[key].channel))
                self.bus_teardown_select.set_options(self.TeardownSelectList)

                self.updateSelectList()
                self.bus_setup_select.set_options(self.SetupSelectList)

        elif ctrl.id == "bus_disconnect":

            self.can_processor.busDict[self.toTeardown].shutdown()
            del self.can_processor.busDict[self.toTeardown]
            del self.can_processor.configDict[self.toTeardown]
            
            self.TeardownSelectList = []
            for key in self.can_processor.configDict.keys():
                self.TeardownSelectList.append((self.can_processor.configDict[key].channel, self.can_processor.configDict[key].channel))
            self.bus_teardown_select.set_options(self.TeardownSelectList)

            self.updateSelectList()
            self.bus_setup_select.set_options(self.SetupSelectList)

            self.query_one("#CAN_connections").query_one("#" + self.toTeardown).remove()
                
    @on(Select.Changed)
    def on_select_changed(self, event:Select.Changed) -> None:
        event.stop()
        ctrl: Select = event.control

        if ctrl.id == "bus_setup_select":
            if event.value == 'pcan':
                log('pcan selected')
                self.bus_config = BusConfig(interface="pcan", channel="PCAN_USBBUS1", bitrate=500000)
            elif event.value == 'virtual':
                log('virtual selected')
                self.bus_config = BusConfig(interface="virtual", channel="test", bitrate=500000)
            else:
                log(f'{event.value} selected')
                self.bus_config = BusConfig(interface="pcan", channel=event.value, bitrate=500000)
        elif ctrl.id == "bus_teardown_select":
            if event.value == "None":
                pass
            else:
                self.toTeardown = event.value

    def updateSelectList(self):
        self.SetupSelectList = []
        for device_id, device_info in self.USBMonitor.get_available_devices().items():
            temp_string = None
            if device_info[ID_MODEL] == "PCAN-USB FD":
                temp_string = "PCAN_USBBUS" + device_id[len(device_id) - 1]
            if temp_string != None:
                if not self.can_processor.busDict.keys().__contains__(temp_string):
                    self.SetupSelectList.append((temp_string, temp_string))
        if not self.can_processor.busDict.keys().__contains__("test"):
            self.SetupSelectList.append(("Virtual","virtual"))