"""Widget for viewing data table of CAN packets"""
import asyncio
import can
import time

from textual import on
from textual import log
from textual.app import ComposeResult
from textual.containers import Center, Vertical, Horizontal, Container
from textual.widgets import Button, DirectoryTree, DataTable, Input, Label, Select, Checkbox

from zeus.config.app_config import BusConfig

class LiveView(Container):
    DEFAULT_CSS = """
    LiveView {
      #data_table {
        height: 50%;
        margin: 2;
        border: round white;
      }
      #bus_connect {
        margin: 1
      }
      Select {
        border: round rgb(11, 127, 204);
      }
      Vertical.scrollable {
        overflow:auto;
      }
      Checkbox {
        margin: 1;
      }
      DirectoryTree {
        height: 30%
      }
    }
    """

    table: DataTable
    bus_connect: Button
    bus_select: Select
    logtype_select: Select
    log_checkbox: Checkbox
    logging_enabled: bool = False
    bus1config: BusConfig
    selected_file: str

    def __init__(self, **kwargs) -> None:
      super().__init__(**kwargs)
      self.table = DataTable(id="data_table", zebra_stripes=True)
      self.bus_connect = Button(id="bus_connect", label="Connect CAN Bus")
      self.bus_select = Select(id="bus_select", prompt="Select CAN Bus Interface", options=[("PCAN","pcan"),("Virtual","virtual")])
      self.bus_select.border_title = "CAN Bus Selection: "
      
      self.logtype_select = Select(id="logtype_select",prompt="Select Log filetype",options=[(".trc",".trc"),(".csv",".csv")])
      self.logtype_select.border_title = "Log Filetype Selection: "
      
      self.log_checkbox = Checkbox(label="Enable Logging", value=self.logging_enabled, id="enable_logging")
      self.bus1config = BusConfig()

    def compose(self) -> ComposeResult:
        
      with Vertical(id="dataview",classes="scrollable"):
          yield self.table
          with Horizontal(id="bus_setup"):
            yield self.bus_connect
            yield self.bus_select
          with Horizontal(id="log_setup"):
            yield self.log_checkbox
            yield self.logtype_select
          yield DirectoryTree(path='.', id="directory_tree")

    def on_mount(self):
      self.table.add_columns("Timestamp","CAN ID", "Rx/Tx", "Length", "Data")
        
      # Add some dummy data:
      self.table.add_row("00:00:01", "0x123", "Rx", "8", "11 22 33 44 55 66 77 88")
      self.table.add_row("00:00:02", "0x456", "Tx", "4", "AA BB CC DD")
      self.table.add_row("00:00:03", "0x789", "Rx", "2", "EE FF")

      self.update_select_visibility()

    @on(Checkbox.Changed)
    def on_checkbox_changed(self, event:Checkbox.Changed) -> None:
      event.stop()
      ctrl: Checkbox = event.control
      if ctrl.id == "enable_logging":
        self.logging_enabled = ctrl.value
      self.update_select_visibility()
      

    def update_select_visibility(self) -> None:
      """Update the visibility of the Select widget based on logging state."""
      if self.logging_enabled:
        self.logtype_select.styles.visibility = 'visible'
      else:
        self.logtype_select.styles.visibility = 'hidden'
    
    @on(Button.Pressed)
    def on_button_press(self, event:Button.Pressed) -> None:
      event.stop()
      ctrl: Button = event.control
      if ctrl.id == "bus_connect":
        self.initializeBus()

    def initializeBus(self):
      self.bus1 = can.Bus(channel=self.bus1config.channel, interface=self.bus1config.interface, bitrate=self.bus1config.bitrate)
    
    async def loadTrace(self, file_path):
        self.table.clear()
        try:
            log_reader = can.LogReader(file_path)
            messages = can.MessageSync(log_reader)

            self.run_worker(self.replayTrace(messages), exclusive=True)
        except Exception as e:
            log("Error with loading trace")

    async def replayTrace(self, message_sync):
        #logger = can.Logger(filename)

        #notifier = can.Notifier(self.bus1)
        
        for msg in message_sync:
          log(f"Got message: {msg}")
          if msg.is_error_frame == False:
            timestamp = f"{msg.timestamp:.3f}"
            can_id = f"{msg.arbitration_id:03X}"
            length = msg.dlc
            data = " ".join(f"{b:02X}" for b in msg.data)
            self.bus1.send(msg)
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

    @on(Input.Submitted)
    async def accept_filename(self):
        input = self.query_one(Input)
        file_path = input.value.strip()
        await self.loadTrace(file_path)
        input.value = ""


    @on(DirectoryTree.FileSelected)
    def handle_file_selected(self, event:DirectoryTree.FileSelected):
      selected_path = str(event.path)
      if selected_path.endswith(".trc",".csv"):
        self.selected_file = selected_path
        self.loadTrace(self.selected_file)
    



    


    

            
