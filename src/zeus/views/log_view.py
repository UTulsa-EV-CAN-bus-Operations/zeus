import asyncio
from pathlib import Path
from textual import on
from textual import log
from textual.app import ComposeResult
from textual.containers import Container, Horizontal, Vertical, ScrollableContainer
from textual.widgets import DirectoryTree, Button, DataTable, Input, Label, Select

from zeus.widgets.titled_container import TitledContainer
from zeus.messages.messages import CANMessageReceived

from zeus.can_processor import CANProcessor
from can import Bus


class LogView(Container):
    
    DEFAULT_CSS = """
    TitledContainer{
        height: auto;
        margin: 1 0 1 0;
        border: round white;
    }
    #left-panel{
        height: auto;
        width: 1fr;
        margin: 0 2;
    }
    #right-panel {
        height: auto;
        width: 2fr;
        margin: 0 2;
    }
    #dir_tree {
        margin: 1 0 1 0;
        border: round white;
    }
    #close_log {
        margin: 1
    }
    """

    """    #data_table {
        height: 30;
        border: round white;
    }"""

    can_processor: CANProcessor
    dir_tree: DirectoryTree
    right_pane: TitledContainer
    selected_replay_path: Path=None
    can_select: Select
    #table: DataTable
    
    def __init__(self, root_dir: str = "./zeus/logs/", **kwargs):
        super().__init__(**kwargs)
        #self.table = DataTable(id="data_table", zebra_stripes=True)
        self.root_dir = root_dir
        self.selected_replay_path = None
        self.dir_tree = DirectoryTree(self.root_dir, id="dir_tree")
        self.can_processor = self.app.can_processor
        self.right_pane = TitledContainer("Type the name of your new log file and press enter to save")

        self.CanSelectList = []
        self.can_select = Select(id="logger_connection", prompt="Select Active CAN Bus Interface", options=self.CanSelectList)

        self.can_to_log = None

    def compose(self) -> ComposeResult:
        with ScrollableContainer():
            with Horizontal():
                with Vertical(id="left-panel"):
                    self.dir_tree.border_title = "Log Directory: "
                    yield self.dir_tree
                    #yield Button(label="Load Replay File", id="load_replay")
                with ScrollableContainer(id="right-panel"):
                    with self.right_pane:
                        yield self.can_select
                        yield Input(placeholder="Enter Here...", id="file_enter")
                        yield Button(label="Close Log File", id="close_log")
    
    def on_show(self):
        self.CanSelectList = []
        for key in self.can_processor.configDict.keys():
            self.CanSelectList.append((self.can_processor.configDict[key].channel, self.can_processor.configDict[key].channel))
        self.can_select.set_options(self.CanSelectList)
    
    @on(Input.Submitted)
    def on_input_submitted(self, event: Input.Submitted) -> None:
        ctrl = event.control
        if (ctrl.id == "file_enter"):
            if self.can_to_log == None:
                log("No Can Selected, Logging Failed")
            else:
                self.can_processor.registerLogger(ctrl.value, self.can_to_log)
                log("Log file name saved!")
                ctrl.value = ""
                self.dir_tree.reload()

    @on(Button.Pressed)
    def on_button_pressed(self, event: Button.Pressed) -> None:
        ctrl = event.control
        if (ctrl.id == "close_log"):
            self.can_processor.closeLogger()
            log("Closed log file")
            self.dir_tree.reload()
    
    @on(Select.Changed)
    def on_select_changed(self, event:Select.Changed) -> None:
        event.stop()
        ctrl: Select = event.control
        if ctrl.id == "logger_connection":
            if event.value == 'virtual':
                log('virtual selected')
                self.can_to_log = "test"
            else:
                log(f'{event.value} selected')
                self.can_to_log = event.value
