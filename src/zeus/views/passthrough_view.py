import asyncio
import can

from textual import on
from textual import log
from textual.app import ComposeResult
from textual.containers import Container, VerticalScroll, Horizontal, Vertical
from textual.widgets import Label, Static, Checkbox, Button, Select, Input

from zeus.widgets.bus_stats import BusStats
from zeus.widgets.titled_container import TitledContainer

from zeus.config.bus_config import BusConfig
from zeus.can_processor import CANProcessor
from can import Bus


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

    can_processor: CANProcessor

    bus1: object 
    bus1_select: Select
    Can1SelectList: list[str]

    bus2: object
    bus2_select: Select
    Can2SelectList: list[str]

    passthrough_Start_Button : Button
    passthrough_Stop_Button : Button

    def __init__(self, root_dir: str = "./zeus/logs/", **kwargs):
        super().__init__(**kwargs)
        # Get connection to can_processor
        self.can_processor = self.app.can_processor

        self.root_dir = root_dir
        self.selected_logging_path = None

        self.Can1SelectList = [(str, str)]
        self.Can2SelectList = [(str, str)]

        self.bus1file = None
        self.bus2file = None

        # CAN Bus 1 Interface Select
        self.bus1_select = Select(id="bus1_select", prompt="Select CAN Bus 1 Interface", options=self.Can1SelectList)
        self.bus1_select.border_title = "CAN Bus 1 Interface Selection: "
        
        # CAN Bus 2 Interface Select
        self.bus2_select = Select(id="bus2_select", prompt="Select CAN Bus 2 Interface", options=self.Can2SelectList)
        self.bus2_select.border_title = "CAN Bus 2 Interface Selection: "

        self.bus1 = None
        self.bus2 = None

        # Setup Buttons for controlling passthrough
        self.passthrough_Start_Button = Button(id = "Start_Passthrough", label= "Start Passthrough")
        self.passthrough_Stop_Button = Button(id = "Stop_Passthrough", label= "Stop Passthrough")

    def compose(self) -> ComposeResult:
        with Horizontal():
            with Vertical():
                with TitledContainer("Select Bus 1:"):
                    with Vertical(id="bus1_setup"):
                        yield self.bus1_select

            with Vertical():
                yield Input(placeholder="Enter Here...", id="file_enter")
                yield self.passthrough_Start_Button
                yield self.passthrough_Stop_Button

            
            with Vertical():
                with TitledContainer("Select Bus 2:"):
                    with Vertical(id="bus2_setup"):
                        yield self.bus2_select

    def on_show(self):
        self.Can1SelectList = []
        self.Can2SelectList = []
        for key in self.can_processor.configDict.keys():
            if key != "test":
                self.Can1SelectList.append((self.can_processor.configDict[key].channel, self.can_processor.configDict[key].channel))
                self.Can2SelectList.append((self.can_processor.configDict[key].channel, self.can_processor.configDict[key].channel))
        self.bus1_select.set_options(self.Can1SelectList)
        self.bus2_select.set_options(self.Can2SelectList)

    @on(Input.Submitted)
    def on_input_submitted(self, event: Input.Submitted) -> None:
        ctrl = event.control
        if (ctrl.id == "file_enter"):
            self.bus1file = "zeus/logs/" + ctrl.value + "_Left" + ".trc"
            self.bus2file = "zeus/logs/" + ctrl.value + "_Right" + ".trc"
            log("Log file name saved!")
            ctrl.value = ""

    @on(Button.Pressed)
    def on_button_press(self, event:Button.Pressed) -> None:
        event.stop()
        ctrl: Button = event.control

        if ctrl.id == "Start_Passthrough":
            self.can_processor.startPassthrough(self.bus1, self.bus2, self.bus1file, self.bus2file)
        elif ctrl.id == "Stop_Passthrough":
            self.can_processor.stopPassThrough()
            pass # TODO: Figure out how to stop passthrough Scripts

    @on(Select.Changed)
    def on_select_changed(self, event:Select.Changed) -> None: #TODO: Fix the logic to only allow one of each at a time -- clw
        event.stop()
        ctrl: Select = event.control

        if ctrl.id == "bus1_select":
            log(f'{event.value} selected')
            self.bus1 = event.value


            self.Can2SelectList = []
            for key in self.can_processor.configDict.keys():
                if key != "test" and key != self.bus1:
                    self.Can2SelectList.append((self.can_processor.configDict[key].channel, self.can_processor.configDict[key].channel))
                if self.bus2 == None:
                    self.bus2_select.set_options(self.Can2SelectList)

        if ctrl.id == "bus2_select":
            log(f'{event.value} selected')
            self.bus2 = event.value


            self.Can1SelectList = []
            for key in self.can_processor.configDict.keys():
                if key != "test" and key != self.bus2:
                    self.Can1SelectList.append((self.can_processor.configDict[key].channel, self.can_processor.configDict[key].channel))
            if self.bus1 == None:    
                self.bus1_select.set_options(self.Can1SelectList)