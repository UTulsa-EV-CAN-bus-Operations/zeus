import asyncio
from pathlib import Path
from textual import on
from textual import log
from textual.app import ComposeResult
from textual.containers import Container, Horizontal, Vertical, ScrollableContainer
from textual.widgets import DirectoryTree, Button, DataTable, Input, Label

from zeus.widgets.titled_container import TitledContainer
from zeus.messages.messages import CANMessageReceived


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

    can_processor: object
    dir_tree: DirectoryTree
    right_pane: TitledContainer
    selected_replay_path: Path=None
    #table: DataTable
    
    def __init__(self, root_dir: str = "./zeus/logs/", **kwargs):
        super().__init__(**kwargs)
        #self.table = DataTable(id="data_table", zebra_stripes=True)
        self.root_dir = root_dir
        self.selected_replay_path = None
        self.dir_tree = DirectoryTree(self.root_dir, id="dir_tree")
        self.can_processor = self.app.can_processor
        self.right_pane = TitledContainer("Type the name of your new log file and press enter to save")

    def compose(self) -> ComposeResult:
        with ScrollableContainer():
            with Horizontal():
                with Vertical(id="left-panel"):
                    self.dir_tree.border_title = "Log Directory: "
                    yield self.dir_tree
                    #yield Button(label="Load Replay File", id="load_replay")
                with ScrollableContainer(id="right-panel"):
                    with self.right_pane:
                        yield Input(placeholder="Enter Here...", id="file_enter")
                        yield Button(label="Close Log File", id="close_log")
                        
    
    @on(Input.Submitted)
    def on_input_submitted(self, event: Input.Submitted) -> None:
        ctrl = event.control
        if (ctrl.id == "file_enter"):
            self.can_processor.registerLogger(ctrl.value)
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
