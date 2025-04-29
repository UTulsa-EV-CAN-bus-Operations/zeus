from pathlib import Path
from textual import on
from textual import log
from textual.app import ComposeResult
from textual.containers import Container, Horizontal, Vertical, ScrollableContainer
from textual.widgets import Label, Static, DirectoryTree, Button

from zeus.widgets.titled_container import TitledContainer


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
    """

    can_processor: object
    dir_tree: DirectoryTree
    right_pane: TitledContainer
    selected_replay_path: Path=None
    
    
    def __init__(self, root_dir: str = ".", **kwargs):
        super().__init__(**kwargs)
        self.root_dir = root_dir
        self.selected_replay_path = None
        self.dir_tree = DirectoryTree(self.root_dir, id="dir_tree")

        self.can_processor = self.app.can_processor

        self.right_pane = TitledContainer(f"Filename: {self.selected_replay_path}")

    def compose(self) -> ComposeResult:
        with ScrollableContainer():
            with Horizontal():
                with Vertical(id="left-panel"):
                    self.dir_tree.border_title = "Select a replay file: "
                    yield self.dir_tree
                    yield Button(label="Load Replay File", id="load_replay")
                with ScrollableContainer(id="right-panel"):
                    with self.right_pane:
                        yield Button(label="Start Replay", id="start_replay")

    @on(DirectoryTree.FileSelected)
    def on_directory_tree_click(self, event: DirectoryTree.FileSelected) -> None:
        if str(event.path).endswith(".trc"):
            self.selected_replay_path = event.path
            log(f"Selected TRC: {self.selected_replay_path}")
            self.right_pane.border_title = f"Filename: {self.selected_replay_path.name}"
        else:
            self.selected_replay_path = None

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "load_replay":
            log("Replay file loading...")
            self.can_processor.load_replay(self.selected_replay_path)
        elif event.button.id == "start_replay":
            log("Replay starts now...")
            self.can_processor.loadTrace(self.selected_replay_path)