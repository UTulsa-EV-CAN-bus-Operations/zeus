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
    bus_select: Select
    bus_stats: BusStats
    bus_connect: Button
    bus_disconnect: Button
    can_processor: CANProcessor
    USBList : list[(str, str)]

    refresh : Button

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # CAN Bus Interface Select
        self.USBList = []
        self.USBMonitor = USBMonitor()
        self.getUSBs() # Get availible USB Connections
        self.SelectList = self.USBList
        self.SelectList.append(("Virtual","virtual"))
        self.bus_select = Select(id="bus_select", prompt="Select CAN Bus Interface", options=self.SelectList)
        self.bus_select.border_title = "CAN Bus Interface Selection: "
        self.bus_connect = Button(id="bus_connect", label="Connect")
        self.bus_disconnect = Button(id="bus_disconnect", label="Disconnect")
        #self.refresh = Button(id = "refresh", label = "Refresh")
        
        # Wire CAN_Processor
        self.can_processor = self.app.can_processor
        self.bus_config = None #self.can_processor.bus1config -- shouldn't exist yet? -- clw 5/11


        self.bus_stats = BusStats(None,None) #BusStats(self.can_processor.bus1, self.bus_config) -- shouldn't exist yet? -- clw 5/11, Maybe needed for changing back to file? -- clw


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

        """with Horizontal():
            with Vertical():
                with TitledContainer("Connect Bus:"):
                    with Vertical(id="bus_setup"):
                        yield self.bus_select
                        with Horizontal(id="bus_setup"):
                            yield self.bus_connect
                            yield self.bus_disconnect
                
                with TitledContainer("Bus Stats: "):
                    with Vertical(id="bus_stats"):
                        yield self.bus_stats

                #yield self.refresh"""

    @on(Button.Pressed)
    def on_button_press(self, event:Button.Pressed) -> None:
        event.stop()
        ctrl: Button = event.control
    
        if ctrl.id == "bus_connect":
            if (self.bus_config!=None):
                self.can_processor.initializeBus(self.bus_config, self.bus_config.channel) # Meow
                self.bus_stats.set_bus(self.can_processor.busDict[self.bus_config.channel],self.can_processor.configDict[self.bus_config.channel])
        elif ctrl.id == "bus_disconnect":
            self.can_processor.busDict[self.bus_config.channel].shutdown() # Might have an issue if the bus is started, user changes input, then tries to stop the bus -- needs testing clw
            self.bus_stats.set_bus(None, None)
        elif ctrl.id == "refresh":
            pass
            #self.bus_select.set_options()
                
    @on(Select.Changed)
    def on_select_changed(self, event:Select.Changed) -> None:
        event.stop()
        ctrl: Select = event.control

        if ctrl.id == "bus_select":
            if event.value == 'pcan':
                log('pcan selected')
                self.bus_config = BusConfig(interface="pcan", channel="PCAN_USBBUS1", bitrate=500000)
            elif event.value == 'virtual':
                log('virtual selected')
                self.bus_config = BusConfig(interface="virtual", channel="test", bitrate=500000)
            else:
                log(f'{event.value} selected')
                self.bus_config = BusConfig(interface="pcan", channel=event.value, bitrate=500000)

    def getUSBs(self):
        self.USBList = []
        for device_id, device_info in self.USBMonitor.get_available_devices().items():
            temp_string = None
            if device_info[ID_MODEL] == "PCAN-USB FD":
                temp_string = "PCAN_USBBUS" + device_id[len(device_id) - 1]
            if temp_string != None:
                self.USBList.append((temp_string, temp_string))
