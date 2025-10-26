import asyncio
from pathlib import Path
from textual import on
from textual import log
from textual.app import ComposeResult
from textual.containers import Container, Horizontal, Vertical, ScrollableContainer
from textual.widgets import DirectoryTree, Button, DataTable, Select

from zeus.widgets.titled_container import TitledContainer
from zeus.messages.messages import CANMessageReceived

from zeus.can_processor import CANProcessor
from can import Bus


class ReplayView(Container):
    
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
    Button {
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
    can_to_replay_on: Bus
    #table: DataTable
    
    def __init__(self, root_dir: str = ".", **kwargs):
        super().__init__(**kwargs)
        #self.table = DataTable(id="data_table", zebra_stripes=True)
        self.root_dir = root_dir
        self.selected_replay_path = None
        self.dir_tree = DirectoryTree(self.root_dir, id="dir_tree")
        self.can_processor = self.app.can_processor
        self.right_pane = TitledContainer(f"Filename: {self.selected_replay_path}")
        
        self.CanSelectList = []
        self.can_select = Select(id="replay_connection", prompt="Select Active CAN Bus Interface", options=self.CanSelectList)

        self.can_to_replay_on = None


    def compose(self) -> ComposeResult:
        with ScrollableContainer():
            with Horizontal():
                with Vertical(id="left-panel"):
                    self.dir_tree.border_title = "Select a replay file: "
                    yield self.dir_tree
                    yield Button(label="Load Replay File", id="load_replay")
                    yield Button(label="Refresh Directory", id="refresh")
                with ScrollableContainer(id="right-panel"):
                    with self.right_pane:
                        yield self.can_select
                        with Horizontal():
                            yield Button(label="Start Replay", id="start_replay")
                            yield Button(label="Start Delayed Replay", id="delayed_replay")
                    #self.table.border_title = "Replay Data: "
                    #yield self.table

    #def on_mount(self) -> None:
    #    self.can_processor.set_replay_view(self)
    #    self.table.add_columns("Timestamp","CAN ID", "Rx/Tx", "Length", "Data")

    def on_show(self):
        self.CanSelectList = []
        for key in self.can_processor.configDict.keys():
            self.CanSelectList.append((self.can_processor.configDict[key].channel, self.can_processor.configDict[key].channel))
        self.can_select.set_options(self.CanSelectList)

    @on(DirectoryTree.FileSelected)
    def on_directory_tree_click(self, event: DirectoryTree.FileSelected) -> None:
        if str(event.path).endswith(".trc"):
            self.selected_replay_path = event.path
            log(f"Selected TRC: {self.selected_replay_path}")
        else:
            self.selected_replay_path = None

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "load_replay":
            log("Replay file loading...")
            self.can_processor.load_replay(self.selected_replay_path)
            self.right_pane.border_title = f"Filename: {self.selected_replay_path.name}"
        elif event.button.id == "start_replay":
            log("Replay starts now...")
            if(self.can_processor.messagesToPlay != None):
                self.can_processor.replay(self.can_to_replay_on)
        elif event.button.id == "delayed_replay":
            asyncio.create_task(self.can_processor.loadTrace(self.selected_replay_path, self.can_to_replay_on))
        elif event.button.id == "refresh":
            self.refresh_tree()

    @on(Select.Changed)
    def on_select_changed(self, event:Select.Changed) -> None:
        event.stop()
        ctrl: Select = event.control
        if ctrl.id == "replay_connection":
            if event.value == 'virtual':
                log('virtual selected')
                self.can_to_replay_on = "test"
            else:
                log(f'{event.value} selected')
                self.can_to_replay_on = event.value
    
    # Refresh the directory tree
    def refresh_tree(self):
        self.dir_tree.reload()
    
    """@on(CANMessageReceived)
    def on_can_message_received(self, event: CANMessageReceived) -> None:
        frame = event.frame
        self.table.add_row(frame.timestamp, frame.can_id, frame.rxtx, str(frame.length), frame.data)
        self.table.scroll_end(animate=False)"""