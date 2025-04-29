"""Widget for viewing data table of CAN packets"""
import asyncio
import time

from textual import on
from textual import log
from textual.app import ComposeResult
from textual.containers import Center, Vertical, Horizontal, Container
from textual.widgets import Button, DirectoryTree, DataTable, Input, Label, Select, Checkbox

from zeus.config.bus_config import BusConfig
from zeus.messages.messages import CANFrame, CANMessageReceived

class LiveView(Container):
  DEFAULT_CSS = """
  LiveView {
    width: 1fr;
    height: 1fr;
    overflow: auto;
    
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
    Checkbox {
      margin: 1;
    }
    DirectoryTree {
      height: 10
    }
  }
  """
  can_processor: object
  table: DataTable
  bus_connect: Button
  bus_select: Select
  logtype_select: Select
  log_checkbox: Checkbox
  logging_enabled: bool = False
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
    self.can_processor = self.app.can_processor

  def compose(self) -> ComposeResult:
      
    with Vertical(id="dataview",classes="scrollable"):
        yield self.table
        with Horizontal(id="bus_setup"):
          yield self.bus_connect
          yield self.bus_select
        with Horizontal(id="log_setup"):
          yield self.log_checkbox
          yield self.logtype_select
        with Horizontal(id="directory_select"):  
          yield DirectoryTree(path='.', id="directory_tree")

  def on_mount(self):
    self.can_processor.set_live_view(self)
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
      self.can_processor.initializeBus()

  @on(DirectoryTree.FileSelected)
  async def handle_file_selected(self, event:DirectoryTree.FileSelected):
    selected_path = str(event.path)
    self.selected_file = selected_path
    
    if selected_path.endswith('.trc'):
      log("This is a .trc file!")
      self.table.clear()
      asyncio.create_task(self.can_processor.loadTrace(self.selected_file))
    
    elif selected_path.endswith('.dbc'):
      self.can_processor.load_dbc(self.selected_file)


  @on(CANMessageReceived)
  def on_can_message_received(self, event: CANMessageReceived) -> None:
      frame = event.frame
      self.table.add_row(frame.timestamp, frame.can_id, frame.rxtx, str(frame.length), frame.data)
      self.table.scroll_end(animate=False)
    