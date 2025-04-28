import asyncio
import can
from can import Bus, MessageSync, LogReader, Logger

from textual import on
from textual import log
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container, Horizontal, Center
from textual.screen import Screen
from textual.widgets import Header, Footer, Input, Select, Button, Label, DataTable
from textual.worker import Worker

import time
import datetime

class ReplayConfig():
    interface = "virtual"
    channel = "test"
    bitrate = 500000

class DataDisplay(Screen):
    CSS_PATH = "DataDisplayScreen.tcss"
    
    def __init__(self, bus1config, bus2config):
        self.bus1config = bus1config
        self.bus2config = bus2config
        self.table = DataTable(zebra_stripes=True)
        super().__init__()
    
    def compose(self) -> ComposeResult:
        yield Header()
        with Center(id="data_table"):
            yield self.table

        with Center(id="replay_control"):
            yield Input(placeholder="Enter file path to CAN trace file...", id="trace_filein")
        yield Footer()

    @on(Input.Submitted)
    async def accept_filename(self):
        input = self.query_one(Input)
        file_path = input.value.strip()
        await self.loadTrace(file_path)
        input.value = ""
    
    
    def initializeBuses(self):
        self.bus1 = can.Bus(channel=self.bus1config.channel, interface=self.bus1config.interface, bitrate=self.bus1config.bitrate)
        self.bus2 = can.Bus(channel=self.bus2config.channel, interface=self.bus2config.interface, bitrate=self.bus2config.bitrate)

    async def loadTrace(self, file_path):
        self.table.clear()
        try:
            log_reader = can.LogReader(file_path)
            messages = can.MessageSync(log_reader)

            self.run_worker(self.replayTrace(messages), exclusive=True)
        except Exception as e:
            log("Error with loading trace")
    
        
    async def replayTrace(self, message_sync):
        
        #filename = 'trc-logs\\TextualReplayTESTlog1PACM-{date:%Y-%m-%d_%H-%M-%S}.trc'.format(date=datetime.datetime.now())
        #logger = can.Logger(filename)

        #notifier = can.Notifier(self.bus1)
        
        for msg in message_sync:
                log(f"Got message: {msg}")
                if msg.is_error_frame == False:
                    timestamp = f"{msg.timestamp:.3f}"
                    can_id = f"{msg.arbitration_id:03X}"
                    length = msg.dlc
                    data = " ".join(f"{b:02X}" for b in msg.data)
                    #self.bus1.send(msg)
                    if (msg.is_rx):
                        rxtx="Rx"
                    else:
                        rxtx="Tx"

                    log(f"Adding row: {timestamp}, {can_id}, Rx, {length}, {data}")
                    self.table.add_row(timestamp, can_id, rxtx, str(length), data)
                    await asyncio.sleep(0.001)

        #time.sleep(1.0)
        #log.write("Shutting down...")
        #notifier.stop()
        self.bus1.shutdown()

    def on_mount(self) -> None:
        self.initializeBuses()
        self.table.add_columns("Timestamp","CAN ID", "Rx/Tx", "Length", "Data")
        
    
    


class ToolApp(App):
    TITLE = "Zeus ϟ"
    BINDINGS = [
        Binding(key="q", action="quit", description="Quit the app"),
        Binding(
            key="question_mark",
            action="help",
            description="Show help screen",
            key_display="?",
        )
    ]

    CSS_PATH = "ConfigScreen.tcss"

    def __init__(self):
        super().__init__()
        self.bus1config = ReplayConfig()
        self.bus2config = ReplayConfig()

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield Label()

        bus1config = Center(id="bus1config")
        bus1config.border_title = "CAN Bus 1 Configuration"
        bus2config = Center(id="bus2config")
        bus2config.border_title = "CAN Bus 2 Configuration"        
        with bus1config:
            yield Select(options=[("pcan", "pcan"), ("virtual", "virtual")], prompt="Select Interface", id="interface")
            yield Select(options=[("PCAN_USBBUS1", "PCAN_USBBUS1"), ("test", "test")], prompt="Select Channel", id="channel")
            yield Select(options=[("500000", "500000")], prompt="Select Bitrate", id="bitrate")
        with bus2config:
            yield Select(options=[("pcan", "pcan"), ("virtual", "virtual")], prompt="Select Interface", id="interface")
            yield Select(options=[("PCAN_USBBUS1", "PCAN_USBBUS1"), ("test", "test")], prompt="Select Channel", id="channel")
            yield Select(options=[("500000", "500000")], prompt="Select Bitrate", id="bitrate")
        with Center(id="start"):
            yield Button(label="Start", id="start")

    @on(Select.Changed)
    def select_changed(self, event: Select.Changed) -> None:
        select_widget = event.select

        # Figure out which container is being selected from
        if(select_widget.parent.id == "bus1config"):
            config = self.bus1config
        elif(select_widget.parent.id == "bus2config"):
            config = self.bus2config
    
        # Edit config
        if(select_widget.id == "interface"):
            config.interface = event.value
        elif(select_widget.id == "channel"):
            config.channel = event.value
        else:
            config.bitrate = int(event.value)
        
        # Debugging purposes
        log(self.bus1config.interface)
        log(self.bus2config.interface)

    def on_button_pressed(self, event:Button.Pressed) -> None:
        self.push_screen(DataDisplay(self.bus1config,self.bus2config))


if __name__ == "__main__":
    app = ToolApp()
    app.run()